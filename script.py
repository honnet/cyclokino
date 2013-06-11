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

if not os.path.exists(fifo_file):
    os.mkfifo(fifo_file)

command = "mplayer -fs -slave -input file=" + fifo_file + " "
os.system( command + movie + "&")

oldspeed=0
MIN_DIF=0.1
MAX_VAL=877.0
OFFSET=0.2

while True:
    speed = int(ser.readline()) / MAX_VAL + OFFSET
#   print "(speed ", speed, ") (old:", oldspeed
#   print "diff ", (speed-oldspeed)

    if (abs(speed-oldspeed) > MIN_DIF):
        os.system("echo speed_set "
                  + str(speed) + " > " + fifo_file)

    oldspeed = speed
    time.sleep(0.5)

