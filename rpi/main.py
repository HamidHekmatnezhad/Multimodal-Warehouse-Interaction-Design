from drivers.ultraSonicHA import ultraGetData
from drivers.lightSensorHA import get_light_sensor, get_threshold
from drivers.lcdHA import change_color, set_color, lcd_write
from drivers.ledsHA import rgb_led
from drivers.buzzerHA import bip
from RPi import GPIO 
from threading import Thread
from time import sleep 

# settings for button interrupt
BTN_PIM = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN_PIM, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pull-up (normal high)

# variables
dist:int = 0
light_bool:bool = False
packet_status:bool = True
packet_corrected:bool = True  # True if packet is correct, False if not

def peak_led_buzzer(clr:str, count:int):
    for _ in range(count):
        rgb_led(clr, True)
        bip(1)
        sleep(0.05)
        rgb_led(clr, False)
        bip(0)
        sleep(0.06)

def refresh_lcd(l1, l2):
        set_color()
        lcd_write(l1, l2)
        sleep(0.1)


def drop_packet_callback(channel):
    """
    Diese Interrupt-Service-Routine wird aufgerufen, wenn der Button gedrückt wird.
    Sie signalisiert dem System (und Unity), dass das Paket 'gedroppt' werden soll.
    """
    print("Button Pressed: Packet Drop Action!")
    # TODO send data to MQTT (drop packet)

def main():
        
    last_light_state = False
    # TODO interrupt for pototiometer to set threshold_light
    # Setup button interrupt
    GPIO.add_event_detect(BTN_PIM, GPIO.FALLING, 
                          callback=drop_packet_callback, 
                          bouncetime=300)

    while True:
        dist = ultraGetData()
        light_bool, val_light_sensor = get_light_sensor()
        threshold_light = get_threshold()
        # TODO get point from MQTT

        # Set LCD display
        point = 4
        l1 = f"dist:{dist:03d} - {val_light_sensor:02d}/{threshold_light:02d}"
        l2 = f"point: {point}"
        lcd = Thread(target=refresh_lcd, args=(l1, l2))
        if not lcd.is_alive():
            lcd.start()
        

        # TODO get packet_status data (corrert data, or not) from MQTT
        # TODO: send data(dist, light_bool) to MQTT
        # TODO get packet_status data from MQTT
        # TODO get packet_corrected data from MQTT
        
        if packet_status:
            rgb_led("green", True)

            if light_bool and not last_light_state:
                if packet_corrected:
                    peak = Thread(target=peak_led_buzzer, args=("green", 1))
                    if not peak.is_alive():
                        peak.start()
                    # TODO send data to MQTT (point and true for action)

                elif not packet_corrected:
                    peak = Thread(target=peak_led_buzzer, args=("red", 3))
                    if not peak.is_alive():
                        peak.start()
                    # TODO send data to MQTT 

            last_light_state = light_bool # ! test
        else:
            rgb_led("green", False)

        sleep(0.1)

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        GPIO.cleanup()