import sys, math, datetime
import serial, string, os
import RPi.GPIO as GPIO
import time
import serial
import io
from time import sleep
from methods import *

"""
This script takes in inputs from button presses and
changes the "theme song" that can be played. Rickshaw drivers
can play their desired song (or stop it) by hitting the toggle button.
"""
try: 
    song_dict = {}
    song_dict[0] = 'roll_up.mp3'
    song_dict[1] = 'purple.mp3'
    song_dict[2] = 'miles_500.mp3'
    print("song dict = " + str(song_dict))

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP) # toggle

    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP) # song 1
    GPIO.setup(4, GPIO.OUT) # button 1, light

    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) # song 2
    GPIO.setup(27, GPIO.OUT) # button 2, light

    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # song 3
    GPIO.setup(10, GPIO.OUT) # button 3, light

    # reset lights
    GPIO.output(4, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(10, GPIO.LOW)

    light_dict = {}
    light_dict[0] = 4
    light_dict[1] = 27
    light_dict[2] = 10
    # set up mpc
    os.system('mpc update')
    os.system('mpc clear')
    os.system('mpc -p 6600')
    os.system('mpc volume 100')
    os.system('mpc repeat off')
    os.system('mpc play')

    curr_song_index = "Nothing"
    curr_light = -1

    while True:
        # read pins, assign to var
        toggle = GPIO.input(2)
        song1 = GPIO.input(3)
        song2 = GPIO.input(17)
        song3 = GPIO.input(22)

        if not toggle and curr_song_index != "Nothing" and not is_playing():
            print("playing " + str(song_dict[curr_song_index]))
            play(curr_song_index, song_dict)
        elif not toggle and curr_song_index == "Nothing":
            print("can't play nothing!")
        elif toggle and is_playing():
            stop()
        elif not song1:
            curr_song_index = 0
            curr_light = switch_lights(curr_light, curr_song_index, light_dict)
            print("song set to 0")
            if is_playing():
                stop()
                play(curr_song_index, song_dict)
        elif not song2:
            curr_song_index = 1
            print("song set to 1")
            curr_light = switch_lights(curr_light, curr_song_index, light_dict)
            if is_playing():
                stop()
                play(curr_song_index, song_dict)
        elif not song3:
            curr_song_index = 2
            print("song set to 2")
            curr_light = switch_lights(curr_light, curr_song_index, light_dict)
            if is_playing():
                stop()
                play(curr_song_index, song_dict)

        sleep(0.1)
except KeyboardInterrupt:
    GPIO.output(4, GPIO.LOW)
    GPIO.output(27, GPIO.LOW)
    GPIO.output(10, GPIO.LOW)
    os.system('mpc clear')




