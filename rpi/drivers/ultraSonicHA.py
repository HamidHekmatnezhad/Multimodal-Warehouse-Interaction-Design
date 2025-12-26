from grovepi import ultrasonicRead

def ultraGetData(pin:int=3):
	"""
	Ermittelt die Distanz mithilfe des Grove-Ultraschallsensors.
    
    Diese Funktion liefert einen kontinuierlichen Datenstrom, der für die 
    isomorphe Metapher im Unity-Lagerszenario verwendet wird (Mapping auf die Z-Achse). 

    Args:
        pin (int): Die Nummer des digitalen Ports am GrovePi+ (Default: D3).
        
    Returns:
        int: Die gemessene Entfernung in Zentimetern (cm).
	"""
	
	try: 
		return ultrasonicRead(pin)
	
	except IOError:
		print("IOError in ultraSonic")
	except:
		print("error in ultraSonic")
		




def test():
	from time import sleep as s
	
	for _ in range(500):
		print(ultraGetData(),"cm")

if __name__ == "__main__":
	test()
