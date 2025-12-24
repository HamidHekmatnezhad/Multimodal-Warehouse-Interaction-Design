from grovepi import pinMode, digitalWrite
from time import sleep

def bip(pin:int=4, duration=0.05):
	"""
	pin=4 (int)
	duration: (s)
	
	retrun NONE
	"""
	try:
		pinMode(pin, "OUTPUT")
			
		digitalWrite(pin, 1)
		sleep(duration)
		digitalWrite(pin,0)
	
	except IOError:
		raise("IOError in buzzer")
	except:
		raise("error in buzzer")	
	
	
	
	
def test():
	
	t = 0.08
	bip()
	sleep(t)
	bip()
	sleep(t)
	bip()
	sleep(t)
	
if __name__ == "__main__":
	test()
	
