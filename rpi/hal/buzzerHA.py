from grovepi import pinMode, digitalWrite

PIN = 4
pinMode(PIN, "OUTPUT")

def beep(mode:int=0):
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
		print("IOError in buzzer")
	except:
		print("error in buzzer")

	
def test():
	from time import sleep
	t = 0.08
	beep()
	sleep(t)
	beep()
	sleep(t)
	beep()
	sleep(t)
	
if __name__ == "__main__":
	test()
	
