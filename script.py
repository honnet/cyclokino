#!/usr/bin/python
import os
import sys
import time
import signal
import serial

# where the playback speed is requested
host = "localhost"
port = "3333"
movie = sys.argv[1] # TODO movie list

def signal_handler(signal, frame):
    print 'Exiting...'
    os.remove(fifo_file)
    print '\nFIFO file removed.'
    os.system("killall mplayer")
    print '\nmplayer killed.'
    sys.exit(0)

ser = serial.Serial('/dev/ttyACM0', 9600);
ser.isOpen()

if not os.path.exists(fifo_file):
    os.mkfifo(fifo_file)

command = "cvlc --extraintf rc --rc-host "
command = command + host + ":" + port + " " + movie + "&"
os.system(command)
print command

oldspeed=0
MIN_DIF=0.1
MAX_VAL=120.0 # to use with the bubble machine (use 930.0 on 24V)
OFFSET=0.2

while True:
    vin = ser.readline()
#   print "vin = ", vin
    speed = int(vin) / MAX_VAL + OFFSET
    speed = int(speed*20) / 20.0 # round to 5%
#   print "(speed:", speed, ") (old:", oldspeed, ") => diff: ", (speed-oldspeed)

    if (abs(speed-oldspeed) > MIN_DIF):
        command = "echo rate " + str(speed) + " | telnet " + host + " " + port + "&"
        os.system(command)
        print command

    oldspeed = speed
    time.sleep(0.3)

