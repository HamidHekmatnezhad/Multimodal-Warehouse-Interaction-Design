from drivers.ultraSonicHA import ultraGetData
from drivers.lightSensorHA import get_light_sensor
from time import sleep 

dist:int = 0
light_bool:bool = False
packet_status:bool = True

def main():

    while True:
        dist = ultraGetData()
        light_bool = get_light_sensor()
        # TODO: update liquid lcd display (dist, packet count)
        # TODO get packet_status data (corrert data, or not) from MQTT
        # TODO: send data(dist, light_bool) to MQTT
        if light_bool:
            if packet_status:
                pass
                # TODO led
                # TODO buzzer
                # TODO send data to MQTT (point and true for action)

            elif not packet_status:
                pass
                # TODO led wrong packet
                # TODO buzzer wrong packet
                # TODO send data to MQTT 
                # TODO push the BTN

        sleep(0.1)

if __name__ == "__main__":
    main()

