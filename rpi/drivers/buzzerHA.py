from grovepi import pinMode, digitalWrite

def bip(mode:int=0, pin:int=4):
	"""
	pin=4 (int)
	mode=0 (int)	1 or 0
	
	retrun NONE
	"""
	try:
		pinMode(pin, "OUTPUT")
		digitalWrite(pin, mode)
	
	except IOError:
		raise("IOError in buzzer")
	except:
		raise("error in buzzer")	
	
	
	
	
def test():
	from time import sleep
	t = 0.08
	bip()
	sleep(t)
	bip()
	sleep(t)
	bip()
	sleep(t)
	
if __name__ == "__main__":
	test()
	
