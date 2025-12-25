from grovepi import pinMode, digitalWrite

PIN = 4
pinMode(PIN, "OUTPUT")

def bip(mode:int=0):
	"""
    Steuert den Buzzer für auditives Feedback an.
    
    Diese Funktion wird genutzt, um dem Nutzer akustische Signale über den 
    Systemstatus zu geben (z. B. Bestätigung eines Scans oder Fehlermeldung).

    Args:
        mode (int): Der Zustand des Buzzers (1 für AN, 0 für AUS).
    """
	try:
		digitalWrite(PIN, mode)
	
	except IOError:
		raise Exception("IOError in buzzer")
	except:
		raise Exception("error in buzzer")

	
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
	
