from grovepi import pinMode, analogRead

def get_light_sensor(pin:int=2):
	"""
	pin=2 (int)
	"""
	try:
		pinMode(pin, "INPUT")
		return analogRead(pin)
		
	except IOError:
		raise("IOError in light sensor")
	except:
		raise("error in light sensor")
		





def test():
	
	for _ in range(800):
		print(get_light_sensor())

if __name__ == "__main__":
	test()
