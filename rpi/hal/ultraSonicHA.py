from grovepi import ultrasonicRead


class ultra_sonic:
	"""
	Klasse zur Steuerung des Ultraschallsensors.
	"""
	def __init__(self, PIN:int):
		self.PIN = PIN
	
	def GetData(self):
		"""
			
		Returns:
			int: Die gemessene Entfernung in Zentimetern (cm).
		"""
		
		try: 
			return ultrasonicRead(self.PIN)
		
		except IOError:
			print("IOError in ultraSonic")
		except:
			print("error in ultraSonic")
			

def test():
	from time import sleep as s
	ut = ultra_sonic(3)
	for _ in range(500):
		print(ut.GetData(),"cm")

if __name__ == "__main__":
	test()
