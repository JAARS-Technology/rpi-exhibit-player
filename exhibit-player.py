#!/usr/bin/python3
#
# exhibit-player.py - play videos based on GPIO selection
#
# Dale Newby
# March 2021
#
# Accept the USB flash disk mount point from the command line.
# dkn November 2022

import vlc
import time
import sys
import os
from gpiozero import Button
from subprocess import check_call

delay = 0.3     # short delay to ensure video is playing

video_index = 0     # index into list of videos

# Directory containing the video files
if len(sys.argv) == 2:
    videodir = sys.argv[1] + "/Videos"
else:
    videodir = '/media/pi/USBDISK/Videos'  # backwards compatible default

# Define the Raspberry Pi GPIO pins used; additional info at:
# https://www.raspberrypi.org/documentation/usage/gpio/
btn_poweroff = 2    # GPIO2, physical pin 3
btn_video1 = 4      # GPIO4, physical pin 7
btn_video2 = 17     # GPIO17, physical pin 11
btn_video3 = 27     # GPIO27, physical pin 13
btn_video4 = 22     # GPIO22, physical pin 15

# Routines used as callbacks when buttons are pressed
def shutdown():
    check_call(['sudo', 'poweroff'])

def request_video1():
    global video_index
    video_index = 1

def request_video2():
    global video_index
    video_index = 2

def request_video3():
    global video_index
    video_index = 3

def request_video4():
    global video_index
    video_index = 4


# Holding the poweroff button for 2 seconds results in the
# Raspberry Pi powering itself off
shutdown_btn = Button(btn_poweroff, hold_time=2)
shutdown_btn.when_held = shutdown

# Pressing a video request button triggers playing the video
video1_btn = Button(btn_video1)
video1_btn.when_pressed = request_video1

video2_btn = Button(btn_video2)
video2_btn.when_pressed = request_video2

video3_btn = Button(btn_video3)
video3_btn.when_pressed = request_video3

video4_btn = Button(btn_video4)
video4_btn.when_pressed = request_video4


# Create the VLC media player object
media_player = vlc.MediaPlayer()
media_player.set_fullscreen(True)

# Get list of video files
# The first file in the list will be used as the default video.
files = os.listdir(videodir)
files.sort()

# Create media objects and record each video's runtime
media_list = []
runtime = []

for ii in files:
    # Create the media object and add it to the list.
    media = vlc.Media(os.path.join(videodir, ii))
    media_list.append(media)

    # Play the video
    media_player.set_media(media) 
    media_player.play() 

    # Get the length of the current video.  The video must be playing
    # before the length is available.
    time.sleep(delay)     # delay to allow video to start playing
    value = media_player.get_length() 
    runtime.append(value)

    #value = media_player.get_time()    # info for debugging only
    #print("Current play time: ", value)


# As long as video_index is zero, play the default video.  Button presses
# will asynchronously change the value of video_index.  Wake up every
# second to check if a video has been requested (via a button press).
while True:
    if (video_index != 0):      # Play requested video
        current = video_index
        video_index = 0
        media_player.set_media(media_list[current]) 
        media_player.play() 
        media_player.audio_set_volume(100)

        for ii in range(int(runtime[current] / 1000) + 1):
            time.sleep(1)
            if (video_index != 0):
                break

    if (video_index == 0):      # Play default video
        media_player.set_media(media_list[0])   # video 0 is the default
        media_player.play() 
        media_player.audio_set_volume(0)

        for ii in range(int(runtime[0] / 1000) + 1):
            time.sleep(1)
            if (video_index != 0):
                break

