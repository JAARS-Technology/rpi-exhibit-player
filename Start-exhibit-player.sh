#!/bin/bash
#
# Start-exhibit-player.sh
#
# Delay the startup of exhibit-player.py to give the system time
# to mount the USB flash drive.
#
# Dale Newby
# March 2021
#
# Pass mount point to exhibit-player.py
# dkn November 2022

sleep 20

# Find where the system mounted the USB flash disk
mountpoint = `mount | grep USBDISK | sed -e 's/.* on //' -e 's/ .*//'`

/home/pi/exhibit-player.py $mountpoint &

