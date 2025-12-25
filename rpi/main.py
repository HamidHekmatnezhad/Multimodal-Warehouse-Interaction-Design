from drivers.ultraSonicHA import ultraGetData
from drivers.lightSensorHA import get_light_sensor, get_threshold, set_threshold
from drivers.lcdHA import lcd_template_write
from drivers.ledsHA import rgb_led
from drivers.buzzerHA import bip
from drivers.potentiometerHA import get_potentiometer

from drivers.btnHA import get_btn

from RPi import GPIO 
from threading import Thread, Lock
from time import sleep 

# settings for button interrupt
BTN_PIM = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN_PIM, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pull-up (normal high)


# variables
dist:int = 0
light_bool:bool = False
packet_status:bool = True # True if packet exists, False if not
packet_corrected:bool = True  # True if packet is correct, False if not

i2c_lock = Lock()

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
    # sleep(0.1)


def drop_packet_callback(channel):
    """
    Diese Interrupt-Service-Routine wird aufgerufen, wenn der Button gedrückt wird.
    Sie signalisiert dem System (und Unity), dass das Paket 'gedroppt' werden soll.
    """
    print("Button Pressed: Packet Drop Action!")
    # TODO send data to MQTT (drop packet)


def watch_potentiometer():
    """
    Überwacht den Poten\tiometerwert und 
        passt den Lichtschwellenwert entsprechend an.
    """
    val = get_potentiometer()
    set_threshold(val)
    # sleep(0.1)

def main():
        
    last_light_state = False
    # Setup button interrupt
    GPIO.add_event_detect(BTN_PIM, GPIO.FALLING, 
                          callback=drop_packet_callback, 
                          bouncetime=300)
    dist = 0
    val_light_sensor = 0
    point = 0
    i = 0
    while True:
        
        dist_last = dist
        val_light_last = val_light_sensor
        point_last = point
        
        with i2c_lock:
            dist = ultraGetData()
            light_bool, val_light_sensor = get_light_sensor()
            threshold_light = get_threshold()
        # TODO get point from MQTT
        point = 4

        # Set LCD display
        '''
        with i2c_lock:
        lcd = Thread(target=refresh_lcd, args=(dist, val_light_sensor, threshold_light, point))
        if not lcd.is_alive():
            lcd.start()
        '''
        # if ((abs(dist - dist_last) >= 11) or (point - point_last >= 1) or (abs(val_light_sensor - val_light_last) >= 7)):
        if (i == 5):
            with i2c_lock:
                refresh_lcd(dist, val_light_sensor, threshold_light, point)
                i = 0
        i +=1
        # Watch potentiometer for threshold adjustment
        '''
        potentiometer = Thread(target=watch_potentiometer)
        if not potentiometer.is_alive():
            potentiometer.start()
        '''
        with i2c_lock:
            watch_potentiometer()
            
        with i2c_lock:
            if (1 == get_btn()):
                print("hey")
    
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
