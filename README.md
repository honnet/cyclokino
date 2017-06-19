Welcome to the CycloKino project !
==================================

This repository contains the poof of concept of an interactive and cyclo-powered mobile cinema.
It is developped as a part of the CarAmazAndes project: www.marcho.net

Purpose of the current code: control the speed of a video with the speed of a bike, here is a video:
www.vimeo.com/69235525

Note: with our "dynamo" system, a bike generates just enough energy for an EEE PC + an LED video projector.


Schematic of the system:
========================

Analog side:
------------
Bike wheel => DC motor, 12V => voltage divider, 5V (50K + 100K resistors)...

Digital side:
-------------
... => ADC (microcontroller) => USB serial => Python => mplayer.


Explanation of the system:
==========================
We use a DC motor (like a dynamo) to charge a battery in order to be electrically independent.
We currently use an Arduino compatible board called [Teensy](www.pjrc.com/teensy) to measure the generated voltage.
This board sends the measures to a python program running in an EEE PC.
This python program plays a video (using mplayer) at a speed that depends on the measures.


Usage:
======

Adjust the maximum received value from the bike (`MAX_VAL`).
Edit the path where you placed your films (`FILMS_PATH`) and run:

    python script.py


Contact:
========
For any question, feel free to contact me: Contact(at)Honnet.eu
