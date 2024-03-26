#!/usr/bin/env python

"""beetbox.py: Trigger script for the BeetBox."""

__author__ = "Scott Garner"
__email__ = "scott@j38.net"

import pygame
import time
import sys  # Import sys module to use exit()

import RPi.GPIO as GPIO
import mpr121

# Use GPIO Interrupt Pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

# Use mpr121 class for everything else
mpr121.TOU_THRESH = 0x30
mpr121.setup(0x5a)

# User pygame for sounds
pygame.mixer.pre_init(44100, -16, 12, 512)
pygame.init()

kick = pygame.mixer.Sound('samples/kick.wav')
kick.set_volume(.65)
snare = pygame.mixer.Sound('samples/snare.wav')
snare.set_volume(.65)
openhh = pygame.mixer.Sound('samples/open.wav')
openhh.set_volume(.65)
closedhh = pygame.mixer.Sound('samples/closed.wav')
closedhh.set_volume(.65)
clap = pygame.mixer.Sound('samples/clap.wav')
clap.set_volume(.65)
cymbal = pygame.mixer.Sound('samples/cymbal.wav')
cymbal.set_volume(.65)

# Track touches and last played timestamps
touches = [0] * 12
last_played = [0] * 12

while True:
    if GPIO.input(7):  # Interupt pin is high
        pass
    else:  # Interupt pin is low
        touchData = mpr121.readData(0x5a)
        for i in range(12):
            if touchData & (1 << i):
                current_time = time.time()
                if current_time - last_played[i] >= 1:  # Cooldown period of 1 second
                    print('Pin ' + str(i) + ' was just touched')
                    if i == 0:
                        kick.play()
                    elif i == 1:
                        snare.play()
                    elif i == 2:
                        openhh.play()
                    elif i == 3:
                        closedhh.play()
                    elif i == 4:
                        clap.play()
                    elif i == 5:
                        cymbal.play()
                    elif i == 11:
                        print('Exiting...')
                        sys.exit()  # Exit the application
                    last_played[i] = current_time
            else:
                if touches[i] == 1:
                    print('Pin ' + str(i) + ' was just released')
                touches[i] = 0
