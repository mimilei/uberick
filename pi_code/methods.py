import sys, math, datetime
import serial, string, os
import RPi.GPIO as GPIO
import time
import serial
import io
from time import sleep
from subprocess import check_output

def play(song_num, song_dict):
    """
    Plays the song listed in song_num index of
    the song_dict
    """
    # os.system('mpc crop')
    os.system('mpc clear')
    os.system('mpc add ' + song_dict[song_num])
    os.system('mpc play')

def is_playing():
    if check_output(["mpc", "current"]) == '':
        return False
    return True
def stop():
    os.system('mpc clear')

def switch_lights(curr_light, new_song_index, light_dict):
    print("curr light = " + str(curr_light))
    if curr_light != -1:
        GPIO.output(curr_light, GPIO.LOW)
    new_light = light_dict[new_song_index]
    print("new light = " + str(new_light))
    GPIO.output(new_light, GPIO.HIGH)
    return new_light
