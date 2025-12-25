# imports libraries
from RPi import GPIO 
from threading import Thread, Lock
from time import sleep 

# import drivers
from drivers.ultraSonicHA import ultraGetData
from drivers.lightSensorHA import get_light_sensor, get_threshold, set_threshold
from drivers.lcdHA import lcd_template_write, set_color
from drivers.ledsHA import rgb_led
from drivers.buzzerHA import bip
from drivers.potentiometerHA import get_potentiometer
from drivers.btnHA import get_btn

# variables
dist:int = 0
light_bool:bool = False
packet_status:bool = True # True if packet exists, False if not
packet_corrected:bool = True  # True if packet is correct, False if not
lcd_rate_show = 5 # refresh rate for lcd display
lcd_rate_counter = 0 # counter for lcd display refresh rate

i2c_lock = Lock() # lock for i2c bus access, to prevent OSError 121

def peak_led_buzzer(clr:str, count:int, gap:float=0.05):
    for _ in range(count):
        rgb_led(clr, True)
        bip(1)
        sleep(gap)
        rgb_led(clr, False)
        bip(0)
        sleep(gap)

def refresh_lcd(dist, val_light_sensor, threshold_light, point):
    lcd_template_write(dist, val_light_sensor, threshold_light, point)

def drop_packet():
    """
    Wenn der Button gedrückt wird, sie signalisiert dem System (und Unity), dass das Paket 'gedroppt' werden soll.
    """
    print("Button Pressed: Packet Drop Action!")
    # TODO send data to MQTT (drop packet)

def watch_potentiometer():
    """
    Überwacht den Potentiometerwert und 
        passt den Lichtschwellenwert entsprechend an.
    """
    val = get_potentiometer()
    set_threshold(val)

def main():
        
    # variables
    last_light_state = False
    event_trigger = True
    dist, val_light_sensor, point = 0, 0, 0

    set_color() # initial set color for lcd

    while True:
        
        point_last = point
        
        with i2c_lock:
            dist = ultraGetData()
            light_bool, val_light_sensor = get_light_sensor()
            threshold_light = get_threshold()
        # TODO get point from MQTT
        point = 4

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
        with i2c_lock:
            watch_potentiometer()
            
        # Watch button press 
        with i2c_lock:
            if (1 == get_btn()):
                drop_packet()
    
        # MQTT 
        # TODO get packet_status data (corrert data, or not) from MQTT
        # TODO: send data(dist, light_bool) to MQTT
        # TODO get packet_status data from MQTT
        # TODO get packet_corrected data from MQTT

        # for test
        packet_status = True
        packet_corrected = True 
        
        if packet_status:
            rgb_led("green", True)

            if light_bool and not last_light_state:
                if packet_corrected:
                    '''
                    peak = Thread(target=peak_led_buzzer, args=("green", 1))
                    if not peak.is_alive():
                        peak.start()
                        '''
                    with i2c_lock:
                        peak_led_buzzer("blue", 1)
                    # TODO send data to MQTT (point and true for action)

                elif not packet_corrected:
                    '''
                    peak = Thread(target=peak_led_buzzer, args=("red", 3))
                    if not peak.is_alive():
                        peak.start()
                    '''
                    with i2c_lock:
                        peak_led_buzzer("red", 3)
                    # TODO send data to MQTT 

            last_light_state = light_bool 
        else:
            rgb_led("green", False)

        sleep(0.1)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        GPIO.cleanup()
