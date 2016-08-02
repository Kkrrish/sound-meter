#!/usr/bin/python

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
## This is an example of a simple sound capture script.
##
## The script opens an ALSA pcm for sound capture. Set
## various attributes of the capture, and reads in a loop,
## Then prints the volume.
##
## To test it out, run it and shout at your microphone:

import alsaaudio, time, audioop
import pygame

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
screensize = (900, 600)
screen=pygame.display.set_mode(screensize)
pygame.display.set_caption("Shout harder.. :D")

#Defining colors
WHITE=(255,255,255)
RED=(255,128,128)
YELLOW=(255,255,128)
BLUE=(0,0,255)

#Loop till close button clicked
done=False
clock=pygame.time.Clock()

margin = 20
samples_per_section = screensize[0]/3 - 2*margin

sound_tracks = [[0]*samples_per_section]*3
max_value = [0]*3

current_section = 0

while not done:

	#Limits CPU usage to max 10 times per second
	#Not required here because already the for loop takes averages over one second
	#clock.tick(10)

	total=0
	#Now we read data from device for around one second
	for i in range(0,100):
            l,data = inp.read()
            if l:
                reading=audioop.max(data, 2)
                total=total+reading
            time.sleep(.00001)

	total=total/30

        sound_tracks[current_section] = sound_tracks[current_section][1:] + [total]
	max_value[current_section] = max(max_value[current_section], total)

	screen.fill(WHITE)

        # draw highlighted section
        pygame.draw.rect(screen,YELLOW,
                         (screensize[0]/3*current_section, 0,
                          screensize[0]/3, screensize[1]))

        for i in range(3):
            sectionx = i*screensize[0]/3 + margin
            #add meet wala last year ka feature
            pygame.draw.rect(screen,RED,(sectionx, screensize[1] - max_value[i],
                                         screensize[0]/3 - 2*margin, max_value[i]))

            #add sumukh vala feature
	    for j in range(0,screensize[0]/3 - 2*margin):
                x = j + sectionx
                y = screensize[1] - sound_tracks[i][j]
	        pygame.draw.rect(screen,BLUE,(x, y, 1, sound_tracks[i][j]))

	#frame flip must happen after all drawing commands
	pygame.display.flip()

	#Set close button event
	for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
            if event.type==pygame.MOUSEBUTTONUP :
                if event.button == 3:
                    # right button pressed, clear all arrays
                    sound_tracks = [[0]*samples_per_section]*3
                    max_value = [0]*3
                    current_section = 0
                else:
                    pos = pygame.mouse.get_pos()
                    current_section = (pos[0] * 3) / screensize[0]
                    print pos, current_section
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
