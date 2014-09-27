#!/usr/bin/python
import os
import sys
import time
import glob
import signal
import serial

DEBUG_PRINT = 1

FILMS_DIR =  "cyclo_films"
FILMS_PATH = "" # "/media/cyclo/*/"     # TODO: test USB drive path
FILMS = FILMS_PATH + FILMS_DIR + "/*"   # TODO: test files / folders

FIFO_FILE = "/tmp/mplayer.fifo"

################################# funktions #######################################
def welcome():
    # TODO: test number of files
    print " *** Movies folder: " + FILMS_DIR + " (at the flash drive root)\n"
    print " *** Press ctrl-c to stop.\n"
    signal.signal(signal.SIGINT, signal_handler)
    time.sleep(1)

# allow clean exit with ctrl-c
def signal_handler(signal, frame):
    print "Ciao!"
    cmd = "killall -9 mplayer &> /dev/null && true"
    execute(cmd)
#   os.remove(FIFO_FILE)
    sys.exit(0)

def serial_init():
    devices = glob.glob("/dev/ttyACM*")
    ser = serial.Serial(devices[0], 115200)
    success = ser.isOpen()
    if not success:
        print "\n!!! Error: serial device not found !!!"
        sys.exit(-1)
    return ser

# execute a command (if in debug mode, print it before)
def execute(cmd):
    err = os.system(cmd)
    if DEBUG_PRINT:
        print "command: " + cmd
        if err:
            print "!!! ERROR !!! (code = " + str(err) + ") \n\n"

# return True if vlc is running by checking in process list
def isRunning():
    proc_list = os.popen("ps -Af").read()      # look for an mplayer process...
    return ("mplayer" and "fifo" in proc_list) # ...with the right args.

# playback speed modulation request
def set_speed(speed):
    cmd = "echo speed_set " + str(speed) + " > " + FIFO_FILE
    execute(cmd)

# start playing at a specified speed (list loop, full screen, remote mode)
def play():
    if not os.path.exists(FIFO_FILE):
        os.mkfifo(FIFO_FILE)
    cmd = "mplayer -msglevel all=-1 -fs -slave -input file=" + FIFO_FILE + " " + FILMS + " &"
    execute(cmd)

def constrain(speed, min_s, max_s):
    if speed < min_s:
        speed = min_s
    elif speed > max_s:
        speed = max_s
    return speed

def get_speed(ser):
    MAX_VAL = 120.0  # TODO: recheck
    OFFSET  = 0.2

    vin = ser.readline()
    ser.flush() # TODO to avoid potential overflow ?

    if DEBUG_PRINT:
        print "\nvin = ", int(vin)

    speed = int(vin) / MAX_VAL + OFFSET
    return int(speed*20) / 20.0 # round to 5%


#################################### main #########################################
def main():
    MIN_DIF  = 0.1
    oldspeed = 0

    welcome()
    ser = serial_init()

    while True: # wait for a ctrl-c interrupt
        speed = get_speed(ser)
        speed = constrain(speed, 0.5, 2)

        if DEBUG_PRINT:
            print "(speed:", speed, ") (old:", oldspeed, ") => diff: ", (speed-oldspeed)

        if (abs(speed-oldspeed) > MIN_DIF):
            if not isRunning():
                play()
            else:
                set_speed(speed)
            oldspeed = speed
        time.sleep(0.3)

if __name__ == "__main__":
    main()

