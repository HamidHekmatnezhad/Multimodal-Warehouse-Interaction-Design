from grovepi import pinMode, analogRead

PIN = 8
pinMode(PIN, "INPUT")

def get_potentiometer():
	"""
	Liest den aktuellen Wert des Potentiometers am analogen Port.
    
    Diese Funktion liefert Rohdaten (0-1023), die für die dynamische 
    Schwellenwertanpassung im Lager-Szenario genutzt werden.
	"""
	try:
		return analogRead(PIN)
		
	except IOError:
		raise Exception("IOError in potentiometer")
	except:
		raise Exception("error in potentiometer")
		





def test():
	
	for _ in range(800):
		print(get_potentiometer())

if __name__ == "__main__":
	test()
