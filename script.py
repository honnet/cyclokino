#!/usr/bin/python
import os
import sys
import time
import signal
import serial

fifo_file = "/tmp/mplayer.fifo"
movie = sys.argv[1] # TODO movie list

def signal_handler(signal, frame):
    os.remove(fifo_file)
    print '\nFIFO file removed.'
    os.system("killall mplayer")
    print '\nmplayer killed.'
    sys.exit(0)

ser = serial.Serial('/dev/ttyACM0', 9600);
ser.isOpen()

command = "mplayer -fs -slave -input file=" + fifo_file + " "
os.system( command + movie + "&")

COEF=0.9
oldspeed=0
MIN_DIF=0.1

while True:
    speed = int(ser.readline()) / 877.0 + 0.2
    speed = speed*COEF + (1-COEF)*oldspeed
#   print "(speed ", speed, ") (old:", oldspeed
#   print "diff ", (speed-oldspeed)

    if (abs(speed-oldspeed) > MIN_DIF):
        os.system("echo speed_set "
                  + str(speed) + " > " + fifo_file)

    oldspeed = speed
    time.sleep(0.5)

