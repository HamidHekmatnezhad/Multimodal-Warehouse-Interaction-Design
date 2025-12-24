from grovepi import pinMode, digitalWrite

def rgb_led(led:str="blue", mode:bool=True, red_pin=7, blue_pin=5, green_pin=8):
	"""
	led: "blue", "red", "green"
	mode: True is "on"  and Flase is "off"
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
			return 0
			
		pinMode(pin, "OUTPUT")
		
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
	

