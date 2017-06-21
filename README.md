# Remote Camera Control
A front-to-back solution for creating your own pan & tilt controlled camera (hardware not included).

# Inspiration
Some buddies and I play DnD every weekend, but one of us plays remotely. We wanted a pan/tilt control camera for him so he could look at what he wanted, but all existing solutions either cost a lot of money or only had 170 degrees of rotation. This DIY solution (can) cost a lot less and is fully customizable.

# The Pieces
1. Pan and tilt camera webserver host with MySQL database, PHP front end, and WebSockets interface
2. Python client to communicate between the webserver host and Arduino controller
3. [Arduino code](https://github.com/gladclef/ArduinoPanAndTiltControl) to manage the pan and tilt motors and communicate with the Python client
4. Web page with simple UI to send pan and tilt coordinates to the PHP front end (iPhone compatible)

# Necessary Hardware:
* server with [LAMP](https://en.wikipedia.org/wiki/LAMP_(software_bundle))
* Arduino and USB cable (I use an Arduino Uno)
* computer client with Python3
* motor assembly and necessary peripherals

# Server Setup
1. Set up a MySQL database and user for the server.
2. Point your web browser to the index.php file. I believe the code will do the rest.
