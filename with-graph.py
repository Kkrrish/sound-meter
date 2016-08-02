"""
roar=alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

while True :
	l,incoming=roar.read()
	if l :
		rms=float(audioop.rms(incoming,2))
		volume=float(1/rms*1000)
		print volume

	else :
		print "deetch.."
	time.sleep(0.5)
"""
#!/usr/bin/python
## This is an example of a simple sound capture script.
##
## The script opens an ALSA pcm for sound capture. Set
## various attributes of the capture, and reads in a loop,
## Then prints the volume.
##
## To test it out, run it and shout at your microphone:

import alsaaudio, time, audioop
#import matplotlib.pyplot as plt
import numpy as np
import pygame
import math

# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
inp.setperiodsize(160)

score=[]
width=0.8

#PyGame initialisations and basic objects
pygame.init()
screenx=1280
screeny=720
size=[screenx,screeny]
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Shout harder.. :D")

#Defining colors
WHITE=(255,255,255)
RED=(255,0,0)
BLUE=(0,0,255)

#Loop till close button clicked
done=False
clock=pygame.time.Clock()

turn=0
loudest=[0,0,0]
startx=50
width=40
sound_track=[]
for i in range(0,startx):
	sound_track.append(0)

while not done:

	#Limits CPU usage to max 10 times per second
	#Not required here because already the for loop takes averages over one second
	#clock.tick(10)

	print turn
	total=0
	#Now we read data from device for around one second
	for i in range(0,100):
		l,data = inp.read()
		if l:
			reading=audioop.max(data, 2)
			total=total+reading
		time.sleep(.00001)
	total=total/100
	temp=sound_track[1:]
	temp.append(total)
	sound_track=temp
	#print total
	loudest[turn]=max(loudest,total)
	bar_height=int(total)

	if turn==0:
		startx=50
	elif turn==1:
		startx=150
	elif turn==2:
		startx=250


	screen.fill(WHITE)
	#add sumukh vala feature
	for i in range(0,startx):
		pygame.draw.rect(screen,BLUE,[i,screeny-100-sound_track[i],1,sound_track[i]])
	#add meet wala last year ka feature
	pygame.draw.rect(screen,RED,[startx,screeny-100-bar_height,width,bar_height])
	
	#frame flip must happen after all drawing commands
	pygame.display.flip()
	
	#Set close button event
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			done=True
		if event.type==pygame.KEYDOWN :
				turn=(turn+1)%3
	"""
	#For matplotlib
	score.append(total)
	x_range=range(len(score))
	plt.bar(x_range,score,width,color="red")
	plt.show()
	plt.ion()
	plt.close('all')
	#"""

pygame.quit()