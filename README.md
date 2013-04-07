Welcome to the CycloKino project !
==================================

Purpose: control the speed of a video with the speed of a bike.
Note: the bike generates enough energy for an EEE PC + LED video projector.
This project is a part of the CarAmazAndes project:
[www.marcho.net](http://www.marcho.net)


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

Contact:
========
For any question, feel free to contact me: drix(at)TangibleDisplay.com

