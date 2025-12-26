from grovepi import pinMode, analogRead

threshold_light_sensor = 100 # 40-550

PIN = 2
pinMode(PIN, "INPUT")

def get_light_sensor(pin:int=2):
	"""
	Überprüft den Helligkeitswert am analogen Eingang zur Erkennung von Paketen.
    
    Diese Funktion dient als Trigger-Mechanismus für den Scan-Prozess im Lager.
    Ein niedriger Lichtwert signalisiert die Anwesenheit eines Pakets (Schattenwurf).

    Args:
        pin (int): Die Nummer des analogen Ports (Default: A2).
        
    Returns:
        bool: True, wenn ein Paket erkannt wurde (Dunkelheit), sonst False.
	"""
	try:
		val = analogRead(PIN)
	
		if  val < threshold_light_sensor:
			return (True, val//10)
		elif val >= threshold_light_sensor:
			return (False, val//10)
		
	except IOError:
		print("IOError in light sensor")
	except:
		print("error in light sensor")

def map_value(x):
	"""
	x von 0-1023 auf 40-550 mappen
	"""
	return int(40 + ((x * 510) / 1023))

def set_threshold(value:int):
	"""
	Passt den Schwellenwert des Lichtsensors basierend auf dem Potentiometer-Eingang an.
    
    Diese Funktion ermöglicht eine Echtzeit-Kalibrierung des Systems, um 
    Umgebungslichteinflüsse im Lager-Szenario zu kompensieren. Dies verbessert 
    die Robustheit der Interaktion (Usability).

    Args:
        value (int): Der vom Potentiometer (Rotary Angle Sensor) gelesene Analogwert (0-1023).
        
    Note:
        Die Variable 'threshold_light_sensor' wird global definiert, damit die 
        Erkennungslogik (get_light_sensor) konsistent darauf zugreifen kann.
	"""
	global threshold_light_sensor
	threshold_light_sensor = map_value(value)

def get_threshold():
	return threshold_light_sensor//10


def test():
	from time import sleep as s
	for _ in range(800):
		a, b = get_light_sensor()
		print(a)
		print(b)
		s(.5)

if __name__ == "__main__":
	test()
