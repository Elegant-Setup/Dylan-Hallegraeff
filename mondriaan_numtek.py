#!/usr/bin/python
import struct, random, wave,operator
from Tkinter import *
# modified from http://pseentertainmentcorp.com/smf/index.php?topic=2034.0

# important values: offset, headerlength, width, height and colordepth
# This is for a Windows Version 3 DIB header
# You will likely want to customize the width and height
samplebar = []
samplepos=0
sample=0
x=0
x1=0
x2=0
x3=0
x4=0
x5=0
color1=""
color2=""
color3=""
size=0
temp_size=0
startx_vert=0
canvas_size=1000
lastpos=0
lastpos_blue=0
startx=0
starty=0
endx=0
endy=0
redbar = []
count=0
count2=0
outline_width=0
def define_color(r,g,b):
	rgb = r, g, b
	new_color = '#%02x%02x%02x' % rgb 
	return(new_color)

def set_color(audio_sample): #kies de kleur op basis van de audio, subtiele variaties voor verhoogd realisme
	r = 35 + audio_sample % 60
	g = 110 + audio_sample % 60
	b = 193 + audio_sample % 60
	blue = define_color(r,g,b)

	r = 252 - audio_sample % 10
	g = 221 - audio_sample % 10
	b = 3 + audio_sample % 10 
	yellow = define_color(r,g,b)

	r = 3 + audio_sample % 5
	g = 7 + audio_sample % 5
	b = 14 + audio_sample % 5
	black = define_color(r,g,b) #volledig zwart bestaat niet in de echte wereld
	
	r = 240 - audio_sample % 5
	g = 234 - audio_sample % 5
	b = 228 - audio_sample % 5
	white = define_color(r,g,b)  #volledig wit bestaat niet in de echte wereld
	

	if audio_sample<(22000-4*(44000/6)):
		color1=black		
	if audio_sample<(22000-4*(44000/6)):
		color1=black
	if (audio_sample>(22000-4*(44000/6))) and (audio_sample<(22000-3*(44000/6))):
		color1=white
	if (audio_sample>(22000-3*(44000/6))) and (audio_sample<(22000-2*(44000/6))):
		color1=blue
	if (audio_sample>(22000-2*(44000/6))) and (audio_sample<(22000-1*(44000/6))):
		color1=yellow		
	if audio_sample>(22000-1*(44000/6)):
		color1=red
	return(color1)

def draw_vert(startx_vert,starty,endy):
	temp_size=0
	startx_vert=(int(canvas_size * startx_vert) / 20 ) * 20 #deelbaar door 20 anders valt het niet goed op 't grid
	for i in range((int(canvas_size * starty) / 20 ) * 20+1,(int(canvas_size * endy) / 20 ) * 20 ,20): #vert
		x=samplebar[i+startx_vert+i]
		color1=set_color(x)
		w.create_rectangle(startx_vert,i,startx_vert+20,i+20,fill=color1,outline=black) #draw vert
	return
if __name__ == '__main__':

	#-------------------------------
	#Init, keuren en canvas
	#-------------------------------
	red = define_color(186,11,1)
	blue = define_color(35,110,193)
	yellow = define_color(252,221,3)
	white = define_color(240,234,228) #volledig wit bestaat niet in de echte wereld
	black = define_color(3,7,14) #volledig zwart bestaat niet in de echte wereld
	waveFile = wave.open('opname.wav', 'r')
	length = waveFile.getnframes()
	for i in range(1,canvas_size*10000,20): #inladen, 10000x canvas size om genoeg punten te nemen
		count=count+1
		waveData = waveFile.readframes(1)
		if count==canvas_size/10:
			data = struct.unpack("<h", waveData)			
			data=data[0]*2
			samplebar.append(data)
			count=0
	master = Tk()
	w = Canvas(master, width=canvas_size, height=canvas_size)
	w.pack()	
	w.create_rectangle(0,0,canvas_size*2,canvas_size*2,fill=white,outline=white) #canvas white
	#-------------------------------
	#Teken kleine verticale regels
	#-------------------------------
	startx_vert=0
	for i in range(1,canvas_size,20): #vert
		temp_size=temp_size+1
		x = samplebar[i]
		color1=set_color(x)
		if color1==red:#als een vertical blok rood is (max) teken dan een horizontale regel
			redbar.append(i)			
			size=(temp_size-2)*20 
			temp_size=0
			for i2 in range(0,canvas_size,20): #horizontaal klein

				#-------------------------------
				#Teken horizontale regels
				#-------------------------------

				x3=samplebar[i2-i] #-1 om per regel nieuwe wave-data op te halen
				color2=set_color(x3)
				startx=startx_vert+i2
				starty=i
				endx=startx_vert+20+i2

				endy=i+20

				w.create_rectangle(startx,starty,endx,endy,fill=color2,outline=black) #draw horizontaal

		w.create_rectangle(startx_vert,i,startx_vert+20,i+20,fill=color1,outline=black) #draw vert

	#grote vul blokken, kijk naar rood, teken daar, check size en vul de regel, door naar de volgende rode
	size=(temp_size*20)-20 #20 per row minus de row zelf
	temp_size=0

	#-------------------------------
	#Teken grote horizontale regels
	#-------------------------------
	lastpos=0
	size=0
	count=0
	for i2 in redbar:
		count=count+1
		size=i2-lastpos
		for i3 in range(10):
			x3=samplebar[count*20*i3] #-1 om per regel nieuwe wave-data op te halen
			color2=set_color(x3)
			startx=i3*size
			starty=lastpos+20
			endy=lastpos+(i2-lastpos)
			endx=startx+size
			if endx > canvas_size: #wel binnen de lijntjes eindigen
				endx=canvas_size-1
			if startx > canvas_size: #wel binnen de lijntjes starten
				startx=canvas_size-1

			w.create_rectangle(startx,starty,endx,endy,fill=color2,outline=black) #draw grote vul blokken
		lastpos=i2

	for i2 in range(1,canvas_size,20): #
		x3=samplebar[i2-i] #-1 om per regel nieuwe wave-data op te halen
		color2=set_color(x3)

	#-------------------------------
	#Teken losse verticale regels
	#-------------------------------
	draw_vert(0.65,0,1)
	#draw_vert(0.61,0.68,0.78)
	draw_vert(0.62,0.72,0.78)
	draw_vert(0.67,0.72,0.78)
	#draw_vert(0.68,0.68,0.78)
	draw_vert(0.4,0.28,0.45)
	#-------------------------------
	#Teken witte border
	#-------------------------------
	w.create_polygon([(1, 1), (1, canvas_size/2), (canvas_size/2, 1)],fill=white,outline=black) #make border
	w.create_polygon([(1, canvas_size), (1, canvas_size/2), (canvas_size/2, canvas_size)],fill=white,outline=black) #make border
	w.create_polygon([(canvas_size, 1), (canvas_size, canvas_size/2), (canvas_size/2, 1)],fill=white,outline=black) #make border
	w.create_polygon([(canvas_size, canvas_size), (canvas_size, canvas_size/2), (canvas_size/2, canvas_size)],fill=white,outline=black) #make border
	x=canvas_size-70
	y=canvas_size-10
	w.create_text(x,y, anchor=W, font="Verdana",text="Numtek")
	mainloop()
