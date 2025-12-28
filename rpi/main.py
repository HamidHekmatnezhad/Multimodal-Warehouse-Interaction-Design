# imports libraries
from RPi import GPIO 
from threading import Thread, Lock
from time import sleep 
import paho.mqtt.client as mqtt

# import drivers
from hal.ultraSonicHA import ultraGetData
from hal.lightSensorHA import get_light_sensor, get_threshold, set_threshold
from hal.lcdHA import lcd_template_write, set_color, change_color
from hal.ledsHA import rgb_led
from hal.buzzerHA import beep
from hal.potentiometerHA import get_potentiometer
from hal.btnHA import get_btn
from utils.load_data import load_data_from_json

# variables
dist:int = 0
point:int = 0
light_bool:bool = False
packet_exist:bool = False # True if packet exists, False if not
packet_corrected:bool = True  # True if packet is correct, False if not
lcd_rate_show = 5 # refresh rate for lcd display
lcd_rate_counter = 0 # counter for lcd display refresh rate
POLLING_INTERVAL = 0.1 # main loop polling interval in seconds

i2c_lock = Lock() # lock for i2c bus access, to prevent OSError 121

# ------------------- MQTT Setup -------------------
MQTT_DATA = load_data_from_json()
USERNAME = MQTT_DATA["username"]
PASSWORD = MQTT_DATA["password"]
BROKER_ADDRESS = MQTT_DATA["broker_address"]
PORT= MQTT_DATA["port"]
KEEPALIVE = MQTT_DATA["keepalive"]

TOPIC_EXIST = MQTT_DATA["topic"]["exist"]["path"] # Listening
EXIT_QOS = MQTT_DATA["topic"]["exist"]["qos"]

TOPIC_CORRECTED = MQTT_DATA["topic"]["corrected"]["path"] # Listening
CORRECTED_QOS = MQTT_DATA["topic"]["corrected"]["qos"]

TOPIC_POINT = MQTT_DATA["topic"]["point"]["path"] # Listening
POINT_QOS = MQTT_DATA["topic"]["point"]["qos"]

TOPIC_DISTANCE = MQTT_DATA["topic"]["distance"]["path"] # Sending
DISTANCE_QOS = MQTT_DATA["topic"]["distance"]["qos"]

TOPIC_LIGHT = MQTT_DATA["topic"]["light_sensor"]["path"] # Sending
LIGHT_QOS = MQTT_DATA["topic"]["light_sensor"]["qos"]

TOPIC_DROP = MQTT_DATA["topic"]["drop"]["path"] # Sending
DROP_QOS = MQTT_DATA["topic"]["drop"]["qos"]

SIGNAL_ON  = MQTT_DATA["signals"]["on"]
SIGNAL_OFF = MQTT_DATA["signals"]["off"]

R = MQTT_DATA["color_lcd"]["red"]
G = MQTT_DATA["color_lcd"]["green"]
B = MQTT_DATA["color_lcd"]["blue"]

del MQTT_DATA  # clean up namespace

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)) # rc=0 means success
    client.subscribe([(TOPIC_EXIST, EXIT_QOS),
                      (TOPIC_CORRECTED, CORRECTED_QOS), 
                      (TOPIC_POINT, POINT_QOS),])

def on_message(client, userdata, msg):
    global packet_exist, packet_corrected, point

    try:
        payload = msg.payload.decode('utf-8')
        
        if msg.topic == TOPIC_EXIST:
            packet_exist = True if payload == SIGNAL_ON else False
        
        elif msg.topic == TOPIC_CORRECTED:
            packet_corrected = True if payload == SIGNAL_ON else False
        
        elif msg.topic == TOPIC_POINT:
            point = int(payload)
        
    except Exception as e:
        print(f"ERROR in on_message(): {e}")

def send_to_mqtt(client, topic, data, qos):
    client.publish(topic, data, qos=qos)


def setup_mqtt():
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_ADDRESS, PORT, KEEPALIVE)
    return client
# ------------------- End of MQTT Setup -------------------

def peak_led_buzzer(clr:str, count:int, gap:float=0.05): 
    for _ in range(count):
        with i2c_lock:
            rgb_led(clr, True)
            beep(1)
        sleep(gap)

        with i2c_lock:
            rgb_led(clr, False)
            beep(0)
        sleep(gap)

def refresh_lcd(dist, val_light_sensor, threshold_light, point):
    lcd_template_write(dist, val_light_sensor, threshold_light, point)

def drop_packet(client):
    """
    Wenn der Button gedrückt wird, sie signalisiert dem System (und Unity), 
        dass das Paket 'gedroppt' werden soll.
    """
    send_to_mqtt(client, TOPIC_DROP, SIGNAL_ON, DROP_QOS)
    Thread(target=peak_led_buzzer, args=("red", 2)).start()

def watch_potentiometer():
    """
    Überwacht den Potentiometerwert und 
        passt den Lichtschwellenwert entsprechend an.
    """
    with i2c_lock:
        val = get_potentiometer()

    if val is not None and 0 <= val <= 1023:
        set_threshold(val)

def main():
    
    # MQTT
    client = setup_mqtt()
    client.loop_start()
    change_color(int(R), int(G), int(B))

    # variables
    last_light_state = False
    event_trigger = True
    dist, val_light_sensor = 0, 0
    global lcd_rate_counter, lcd_rate_show, light_bool
    global packet_exist, packet_corrected, point

    set_color() # initial set color for lcd

    while True:
        
        point_last = point
        threshold_light = get_threshold()

        with i2c_lock:
            light_bool, val_light_sensor = get_light_sensor()

        with i2c_lock:
            dist = ultraGetData()
        send_to_mqtt(client, TOPIC_DISTANCE, str(dist), DISTANCE_QOS)


        # Set LCD display
        if (light_bool != last_light_state) or (point != point_last):
            event_trigger = True

        if (lcd_rate_counter >= lcd_rate_show) or event_trigger:
            with i2c_lock:
                refresh_lcd(dist, val_light_sensor, threshold_light, point)
            lcd_rate_counter = 0
            event_trigger = False
        else:
            lcd_rate_counter += 1

        # Watch potentiometer for threshold adjustment
        if (lcd_rate_counter >= lcd_rate_show):
            watch_potentiometer()
            
        # Watch button press 
        with i2c_lock:
            if (1 == get_btn()):
                drop_packet(client)
    
        # for test
        # packet_exist = True
        # packet_corrected = True 
        
        if packet_exist:
            with i2c_lock:
                rgb_led("green", True)

            if light_bool and not last_light_state: # rising edge
                if packet_corrected:
                    send_to_mqtt(client, TOPIC_LIGHT, SIGNAL_ON, LIGHT_QOS)
                    Thread(target=peak_led_buzzer, args=("green", 1)).start()

                elif not packet_corrected:
                    Thread(target=peak_led_buzzer, args=("red", 3)).start()

            last_light_state = light_bool 
        else:
            with i2c_lock:
                rgb_led("green", False)

        sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program interrupted by user. Exiting...")
        exit(0)

    except Exception as e:
        GPIO.cleanup()
        print(f"An error occurred: {e}")
        exit(1)
