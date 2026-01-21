# USELESS

from grovepi import pinMode, digitalWrite

class leds:
	"""
	Klasse zur Steuerung der LEDs.
	"""
	def __init__(self):
		self.blue_pin = 5
		self.red_pin = 7

		pinMode(self.blue_pin, "OUTPUT")
		pinMode(self.red_pin, "OUTPUT")

	def rgb_led(self, led:str="blue", mode:bool=True):
		"""
		Steuert die verschiedenen LEDs zur visuellen Signalisierung des Systemstatus.
		
		Diese Funktion ermöglicht eine klare Benutzerführung durch Farbcodierung:
		- Grün: Paket im Lager vorhanden (Bereitschaft).
		- Blau: Erfolgreicher Scan-Vorgang (Bestätigung).
		- Rot: Fehlerhafter Vorgang oder falsches Paket (Warnung).

		Args:
			led (str): Die Farbe der LED ("red", "green", "blue").
			mode (bool): True schaltet die LED ein (High), False schaltet sie aus (Low).
		"""
		try:
			if led == "blue":
				pin = self.blue_pin
			elif led == "red":
				pin = self.red_pin
			else:
				print("led str uncorrect")
				
			if mode:
				digitalWrite(pin, 1)
			else:
				digitalWrite(pin, 0)
			
		except IOError:
			print("IOError in leds")
		except:
			print("error in leds")






def test():
	from time import sleep as s
	leds = leds()
	leds.rgb_led("red", True)
	leds.rgb_led("blue", True)
	leds.rgb_led("green", True)
	
	s(3)

	leds.rgb_led("red", False)
	leds.rgb_led("blue", False)
	leds.rgb_led("green", False)

if __name__ == "__main__":
	test()
	

