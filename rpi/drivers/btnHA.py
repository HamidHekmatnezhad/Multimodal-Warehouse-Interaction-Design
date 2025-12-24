from grovepi import pinMode, digitalRead

def get_btn(pin:int=6):
	"""
	pin=6 (int)
	
	return 
	"""
	try:
		pinMode(pin, "INPUT")
		return digitalRead(pin)	
		
	except IOError:
		raise("IOError in btn")
	except:
		raise("error in btn")





def test():
	for _ in range(500):
		print(get_btn())
	
if __name__ == "__main__":
	test()
