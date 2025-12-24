from grovepi import pinMode, analogRead

def get_potentiometer(pin:int=8):
	"""
	pin=8 (int)
	"""
	try:
		pinMode(pin, "INPUT")
		return analogRead(pin)
		
	except IOError:
		raise("IOError in potentiometer")
	except:
		raise("error in potentiometer")
		





def test():
	
	for _ in range(800):
		print(get_potentiometer())

if __name__ == "__main__":
	test()
