# imports libraries
from RPi import GPIO 
from threading import Thread, Lock
from time import sleep 
import paho.mqtt.client as mqtt
from json import dumps as json_dumps

# import drivers
from hal.ultraSonicHA import ultra_sonic
from hal.lightSensorHA import light_sensor
from utils.load_data import load_data_from_json

# variables
axe_x:int = 0
axe_y:int = 0
axe_z:int = 0

light_sensor_1_bool:bool = False
light_sensor_2_bool:bool = False
val_light_sensor_1:int = 0
val_light_sensor_2:int = 0

POLLING_INTERVAL = 0.1 # main loop polling interval in seconds

i2c_lock = Lock() # lock for i2c bus access, to prevent OSError 121

# ------------------- MQTT Setup -------------------
MQTT_DATA = load_data_from_json()
USERNAME = MQTT_DATA["username"]
PASSWORD = MQTT_DATA["password"]
BROKER_ADDRESS = MQTT_DATA["broker_address"]
PORT= MQTT_DATA["port"]
KEEPALIVE = MQTT_DATA["keepalive"]

SIGNAL_ON  = MQTT_DATA["signals"]["on"]
SIGNAL_OFF = MQTT_DATA["signals"]["off"]

TOPIC_DATA = MQTT_DATA["topic"]["data"]["path"] # Sending
QOS_DATA = MQTT_DATA["topic"]["data"]["qos"]

PIN_AXE_X = MQTT_DATA["pins"]["axe_x"]
PIN_AXE_Y = MQTT_DATA["pins"]["axe_y"]
PIN_AXE_Z = MQTT_DATA["pins"]["axe_z"]
PIN_LIGHT_SENSOR_1 = MQTT_DATA["pins"]["light_sensor_1"]
PIN_LIGHT_SENSOR_2 = MQTT_DATA["pins"]["light_sensor_2"]
THRESHOLD_LIGHT_SENSOR_1 = MQTT_DATA["thresholds_light_sensor"]["1"]
THRESHOLD_LIGHT_SENSOR_2 = MQTT_DATA["thresholds_light_sensor"]["2"]

del MQTT_DATA  # clean up namespace

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)) # rc=0 means success
    client.subscribe([(TOPIC_DATA, QOS_DATA),])

# def on_message(client, userdata, msg):
#     global packet_exist, packet_corrected, point

#     try:
#         payload = msg.payload.decode('utf-8')
        
#         if msg.topic == TOPIC_EXIST:
#             packet_exist = True if payload == SIGNAL_ON else False
        
#         elif msg.topic == TOPIC_CORRECTED:
#             packet_corrected = True if payload == SIGNAL_ON else False
        
#         elif msg.topic == TOPIC_POINT:
#             point = int(payload)
        
#     except Exception as e:
#         print(f"ERROR in on_message(): {e}")

def send_to_mqtt(client, topic, data, qos):
    client.publish(topic, data, qos=qos)


def setup_mqtt():
    client = mqtt.Client()
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    # client.on_message = on_message
    client.connect(BROKER_ADDRESS, PORT, KEEPALIVE)
    return client
# ------------------- End of MQTT Setup -------------------


def main():
    
    # MQTT
    client = setup_mqtt()
    client.loop_start()

    # variables
    global axe_x, axe_y, axe_z
    global light_sensor_1_bool, light_sensor_2_bool

    # init class
    us_x = ultra_sonic(PIN_AXE_X)
    us_y = ultra_sonic(PIN_AXE_Y)
    us_z = ultra_sonic(PIN_AXE_Z)
    ls_1 = light_sensor(PIN_LIGHT_SENSOR_1, THRESHOLD_LIGHT_SENSOR_1)
    ls_2 = light_sensor(PIN_LIGHT_SENSOR_2, THRESHOLD_LIGHT_SENSOR_2)

    while True:
        
        with i2c_lock:
            axe_x = us_x.GetData()

        with i2c_lock:
            axe_y = us_y.GetData()

        with i2c_lock:
            axe_z = us_z.GetData()

        with i2c_lock:
            light_sensor_1_bool, val_light_sensor_1 = ls_1.getData()

        with i2c_lock:
            light_sensor_2_bool, val_light_sensor_2 = ls_2.getData()

        dt = {
            "axe_x": axe_x,
            "axe_y": axe_y,
            "axe_z": axe_z,
            "light_sensor_1": SIGNAL_ON if light_sensor_1_bool else SIGNAL_OFF,
            "light_sensor_2": SIGNAL_ON if light_sensor_2_bool else SIGNAL_OFF,
        }
        data = json_dumps(dt)

        send_to_mqtt(client, TOPIC_DATA, data, QOS_DATA)

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
