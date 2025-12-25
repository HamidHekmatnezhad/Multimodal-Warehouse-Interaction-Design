from grove_rgb_lcd import setRGB, setText
		
r = 0
g = 150
b = 150

def change_color(red:int, green:int, blue:int):
	"""
	Aktualisiert die globalen Farbwerte für die LCD-Hintergrundbeleuchtung.
    
    Dies ermöglicht eine dynamische visuelle Kodierung des Systemstatus 
    (z. B. Rot für Fehler, Grün für Erfolg).

    Args:
        red (int): Der rote Farbwert (0-255).
        green (int): Der grüne Farbwert (0-255).
        blue (int): Der blaue Farbwert (0-255).
	"""
	global r,g,b 
	r = red
	g = green
	b = blue
	
def set_color():
	"""
    Wendet die aktuell gespeicherten RGB-Werte auf das physische Display an.
    Dient der konsistenten visuellen Rückmeldung während der Interaktion.
    """
	setRGB(r, g, b)
	
def lcd_write(line1:str="", line2:str=""):
	"""
    Schreibt zwei Textzeilen auf das LCD.
    Verwendet das Zeilenumbruchzeichen, um die Informationshierarchie des Displays zu nutzen.

	Args:
		line1 (str): Text für die erste Zeile.
		line2 (str): Text für die zweite Zeile.
    """
	setText(line1 + "\n" + line2)
	
def lcd_template_write(dist:int, val_light_sensor:int, threshold_light:int, point:int):
	"""
    Spezialisierte Funktion für das Warehouse-Interface-Layout.
    
    Diese Funktion implementiert ein festes Layout zur Maximierung der Lesbarkeit (Readability).
    Durch die Formatierung (:03d / :02d) bleibt die Anzeige stabil und verhindert visuelles Flackern.

	Args:
		dist (int): Der gemessene Abstandswert.
		val_light_sensor (int): Der aktuelle Wert des Lichtsensors.
		threshold_light (int): Der eingestellte Schwellenwert für den Lichtsensor.
		point (int): Die aktuelle Punktzahl oder ein ähnlicher Metrikwert.
	
	Templates:
	- Zeile 1: "dist: XXX |SV/TH"
	- Zeile 2: "point: XX |YY/ZZ"
    """

	l1 = f"dist: {dist:03d} |SV/TH"
	l2 = f"point: {point:02d} |{val_light_sensor:02d}/{threshold_light:02d}"
	lcd_write(l1, l2)


def test():
	from time import sleep
	while True:
		r = int(input("r: "))
		g = int(input("g: "))
		b = int(input("b: "))
		t1 = input("line1: ")
		t2 = input("line2: ")
		

		setRGB(r,g,b)
		setText(t1 + "\n" + t2)
		sleep(.1)

if __name__ == "__main__":
	test()


