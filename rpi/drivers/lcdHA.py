from grove_rgb_lcd import setRGB, setText
from time import sleep 
			
			
r = 0
g = 150
b = 150

def change_color(red:int, green:int, blue:int):
	global r,g,b 
	r = red
	g = green
	b = blue
	
def set_color():
	setRGB(r, g, b)
	
def lcd_write(line1:str="", line2:str=""):
	setText(line1 + "\n" + line2)
	



def test():

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
