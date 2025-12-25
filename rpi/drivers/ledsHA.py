from grovepi import pinMode, digitalWrite

blue_pin = 5
red_pin = 7
green_pin = 8

pinMode(blue_pin, "OUTPUT")
pinMode(red_pin, "OUTPUT")
pinMode(green_pin, "OUTPUT")

def rgb_led(led:str="blue", mode:bool=True):
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
			pin = blue_pin
		elif led == "red":
			pin = red_pin
		elif led == "green":
			pin = green_pin
		else:
			raise("led str uncorrect")
			
		if mode:
			digitalWrite(pin, 1)
		else:
			digitalWrite(pin, 0)
		
	except IOError:
		raise("IOError in leds")
	except:
		raise("error in leds")






def test():
	from time import sleep as s
	
	rgb_led("red", True)
	rgb_led("blue", True)
	rgb_led("green", True)
	
	s(3)
	
	rgb_led("red", False)
	rgb_led("blue", False)
	rgb_led("green", False)
	
if __name__ == "__main__":
	test()
	

