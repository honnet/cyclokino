#!/usr/bin/python
import os
import sys
import time
import signal

fifo_file = "/tmp/mplayer.fifo"
movie = sys.argv[1] # TODO movie list

def signal_handler(signal, frame):
    os.remove(fifo_file)
    print '\nFIFO file removed.'
    os.system("killall mplayer")
    print '\nmplayer killed.'
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
os.mkfifo(fifo_file)

command = "mplayer -slave -input file=" + fifo_file + " " # TODO use -fs for full screen
os.system( command + movie + "&")

step = 0.05
speed = 1
while True:
    print "\n => " + str(speed) + "\n"
    os.system("echo speed_set " + str(speed) + " > " + fifo_file)
    if (speed <= 0.5): step = abs(step)
    elif (speed >= 2): step = -abs(step)
    speed += step
    time.sleep(0.1)

