from grovepi import ultrasonicRead

def ultraGetData(pin:int=3):
	"""
	pin=3 int
	retrun cm(int) 
	"""
	
	try: 
		return ultrasonicRead(pin)
	
	except IOError:
		raise("IOError in ultraSonic")
	except:
		raise("error in ultraSonic")
		




def test():
	from time import sleep as s
	
	for _ in range(500):
		print(ultraGetData(),"cm")

if __name__ == "__main__":
	test()
