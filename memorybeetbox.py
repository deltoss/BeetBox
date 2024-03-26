#!/usr/bin/env python

"""beetbox.py: Trigger script for the BeetBox."""

__author__ = "Scott Garner"
__email__ = "scott@j38.net"

import pygame
import time
import random
import sys  # Import sys module to use exit()

import RPi.GPIO as GPIO
import mpr121

# Use GPIO Interrupt Pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)  # Pin 7 for exiting the program

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

# Define sound list
sounds = [kick, snare, openhh, closedhh, clap, cymbal]

def play_sequence(sequence):
    for sound_index in sequence:
        sounds[sound_index].play()
        time.sleep(2)

def get_player_sequence():
    player_sequence = []
    while len(player_sequence) < len(sequence):
        touchData = mpr121.readData(0x5a)
        if touchData & (1 << 7):  # Check if pin 7 is touched to exit
            print("Exiting...")
            GPIO.cleanup()
            sys.exit()
        elif touchData & (1 << 6):  # Check if pin 6 is touched to restart the game
            print("Restarting the game...")
            return None  # Return None to indicate game restart
        else:
            for i in range(12):
                if i != 7 and touchData & (1 << i):
                    sounds[i].play()
                    player_sequence.append(i)
                    time.sleep(0.5)  # Short delay to avoid registering multiple touches
    return player_sequence

while True:
    # Generate a random sequence of sounds
    sequence_length = random.randint(3, 4)
    sequence = [random.randint(0, 5) for _ in range(sequence_length)]

    # Play the random sequence
    play_sequence(sequence)

    # Get player's sequence
    player_sequence = get_player_sequence()

    # Check if the game needs to be restarted
    if player_sequence is None:
        continue  # Restart the game

    # Compare sequences
    if sequence == player_sequence:
        print("Congratulations! You matched the sequence.")
    else:
        print("Wrong sequence! Playing kick sound.")
        kick.play()

    # Wait until pin 7 is pressed before exiting
    print("Press pin 7 to exit or pin 6 to restart...")
    while not (mpr121.readData(0x5a) & ((1 << 7) | (1 << 6))):  # Wait until pin 6 or pin 7 is pressed
        pass

    if mpr121.readData(0x5a) & (1 << 7):  # If pin 7 is pressed, exit the program
        print("Exiting...")
        GPIO.cleanup()
        sys.exit()
    elif mpr121.readData(0x5a) & (1 << 6):  # If pin 6 is pressed, restart the game
        print("Restarting...")
