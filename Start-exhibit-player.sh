#!/bin/bash
#
# Start-exhibit-player.sh
#
# Delay the startup of exhibit-player.py to give the system time
# to mount the USB flash drive.
#
# Dale Newby
# March 2021

sleep 20
/home/pi/exhibit-player.py &

