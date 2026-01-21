from grovepi import pinMode, analogRead

class light_sensor:
	"""
	Klasse zur Steuerung des Lichtsensors.
	"""
	def __init__(self, PIN:int, threshold_light_sensor:int=100):
		self.PIN = PIN
		self.threshold_light_sensor = threshold_light_sensor
		pinMode(self.PIN, "INPUT")

	def getData(self):
		"""
		Überprüft den Helligkeitswert am analogen Eingang zur Erkennung von Paketen.
		
		Diese Funktion dient als Trigger-Mechanismus für den Scan-Prozess im Lager.
		Ein niedriger Lichtwert signalisiert die Anwesenheit eines Pakets (Schattenwurf).
			
		Returns:
			bool: True, wenn ein Paket erkannt wurde (Dunkelheit), sonst False.
		"""
		try:
			val = analogRead(self.PIN)
		
			if  val < self.threshold_light_sensor:
				return (True, val)
			elif val >= self.threshold_light_sensor:
				return (False, val)
			
		except IOError:
			print("IOError in light sensor")
		except:
			print("error in light sensor")

	def set_threshold(self, value:int):
		"""
		Diese Funktion ermöglicht eine Echtzeit-Kalibrierung des Systems, um 
		Umgebungslichteinflüsse im Lager-Szenario zu kompensieren. Dies verbessert 
		die Robustheit der Interaktion (Usability).

		Args:
			value (int): Der vom Potentiometer (Rotary Angle Sensor) gelesene Analogwert (0-1023).
		"""
		self.threshold_light_sensor = value

	def get_threshold(self):
		return self.threshold_light_sensor
	
	def get_pin(self):
		return self.PIN


def test():
	from time import sleep as s
	ls = light_sensor(2)
	for _ in range(800):
		a, b = ls.get_light_sensor_value()
		print(a)
		print(b)
		s(.5)

if __name__ == "__main__":
	test()
