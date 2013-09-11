#!/usr/bin/python
import os
import sys
import time
import glob
import signal
import serial
import random
import platform

DEBUG_PRINT = 1

#################################### init #########################################
FILMS_LIST = "media/*"

PLATFORM = platform.system()
if "Darwin" in PLATFORM:
    VLC_PROC = "VLC"
    VLC_EXEC = "/Applications/VLC.app/Contents/MacOS/VLC"
    PORT_PATTERN = "/dev/tty.usbmodem*"                       # "/dev/cu.usbmodem*" ?
elif "Linux" in PLATFORM:
    VLC_PROC = "vlc"
    VLC_EXEC = VLC_PROC
    PORT_PATTERN = "/dev/ttyACM*"
else:
    print "!!! Error: platform not supported !!!"
    sys.exit(-1)

devices = glob.glob(PORT_PATTERN)
try:
    ser = serial.Serial(devices[0], 9600)
    ser.isOpen()                                              # TODO: check if useful
except:
    print "!!! Error: serial device not found !!!"
    sys.exit(-1)

HOST_PORT = "localhost:3333"

################################# funktions #######################################
# execute a command (if in debug mode, print it before)
def execute(cmd):
    if DEBUG_PRINT:
        print cmd
    print os.system(cmd)

# return True if vlc is running by checking in process list
def isRunning():
    proc_list = os.popen("ps -Af").read()        # look for a vlc process...
    return (VLC_PROC and HOST_PORT in proc_list) # ...with the right args.

# playback speed modulation request
def set_speed(speed):
    cmd = "echo rate {} | nc {}".format(speed, HOST_PORT.replace(':', ' '))
    execute(cmd)

# kill the player !
def quit():
    cmd = "killall -9 " + VLC_PROC
    execute(cmd)

# start playing at a specified speed (list loop, full screen, remote mode)
def play(speed):
    args = " --loop -f -I rc --rc-host {} {}&".format(HOST_PORT, FILMS_LIST)
    execute(VLC_EXEC + args)
    set_speed(speed)

# allow clean exit with ctrl-c
def signal_handler(signal, frame):
    quit()
    sys.exit(0)

#################################### loop #########################################
MIN_DIF=0.1
MAX_VAL=120.0 # to use with the bubble machine (use 930.0 on 24V)
OFFSET=0.2
oldspeed=0

print " *** Movies should be in the specified folder: " + FILMS_LIST
print " *** Press ctrl-c to stop."
time.sleep(1)

while True: # wait for a ctrl-c interrupt
    vin = ser.readline()
#   print "vin = ", vin
    speed = int(vin) / MAX_VAL + OFFSET
    speed = int(speed*20) / 20.0 # round to 5%
#   print "(speed:", speed, ") (old:", oldspeed, ") => diff: ", (speed-oldspeed)

    if speed > 0.5 and speed < 2:
        if not isRunning():
            play(speed)
        elif (abs(speed-oldspeed) > MIN_DIF):
            set_speed(speed)
        oldspeed = speed

    time.sleep(0.3)

