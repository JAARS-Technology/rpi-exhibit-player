# exhibit-player - play videos selected by pressing a button

## Background

A museum exhibit has a large wall-mounted TV monitor.
The exhibit designer has placed momentary contact button switches within
the exhibit which the visitor can press to select a video to be played
on the monitor.
Exhibits change over time and the museum staff will need to change the set
of videos available to be played.

## Requirements

- The system will start playing the default video automatically when powered on.
- The default video will play continuously until a visitor requests a video.
- The default video will play without sound to avoid annoying the museum staff.
- The screen will be black/blank between videos.
- Videos will play full screen.
- The computer desktop is never visible.
- Museum staff can configure which videos will be played.

## Implementation

The switches are connected to the General Purpose I/O (GPIO) of a
Raspberry Pi 3B+ (RPi) running Raspberry Pi OS.
The RPi drives the TV monitor via its HDMI port.
A Python script uses the `gpiozero` module to monitor the GPIO
for button presses and the `vlc` module to play the videos.
The video files are stored in a well-known location on a USB flash drive
and named such that they sort in the desired order.
The first file is used as the default video.

## Materials needed

- [Raspberry Pi 3B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) (other models may work)
- [Raspberry Pi Universal Power Supply](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/) (5V, 2.5A) or equivalent
- (Optional) Case for Raspberry Pi 3 that allows access to the GPIO pins 
- 8 GB microSD card
- USB flash drive to contain the video files
- HDMI cable
- TV monitor with HDMI input
- wire to connect the switches to the GPIO pins
- additional switch to use as a power off request
- mounting hardware as required
- During installation and configuration you will need a USB keyboard and mouse.

## Installation

Download [Raspberry Pi OS with Desktop](https://www.raspberrypi.org/software/operating-systems/) and install it in the usual way. For details, follow the instructions in the [Raspberry Pi Getting Started Guide](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up). The system does not use the network when displaying videos so you can skip the WiFi setup. However, you will need Internet access during the setup. The system was tested with the Raspberry Pi OS released on March 4, 2021. The *full* version is not required as we will not be using all of the additional applications.

After the startup wizard has completed the initial configuration and rebooted
the system, perform the following additional configuration actions.

- Install the Python vlc module.
```bash
	sudo pip3 install python-vlc
```
- Menu > Preferences > Raspberry Pi Configuration
	- System tab: Hostname: *optionally change the hostname*
	- System tab: Boot: `To Desktop`
	- System tab: Auto login: `Login as user 'pi'`
	- System tab: Network at Boot: `Do not wait`
	- System tab: Splash Screen: `Enable`
	- Display tab: Overscan: `Enable`
	- Display tab: Pixel Doubling: `Disable`
	- Display tab: Screen Blanking: `Disable`
	- Interfaces tab: SSH: `Disable`
- Menu > Preferences > Appearance Settings
	- Desktop tab: Layout: `No image`
	- Desktop tab: Colour: Colour name: `#000000`
	- Desktop tab: clear `Documents`, `Wastebasket`, `External Disks`
	- Menu Bar tab: Colour: Colour name: `#000000`
	- Menu Bar tab: Text Colour: Colour name: `#EDECEB`
- Right click the Task Bar > Panel Settings
	- Advanced tab: select `Minimize panel when not in use`
- Copy `exhibit-player.py` and `Start-exhibit-player.sh` to `/home/pi/`. Ensure both files are executable: 
```bash
	chmod +x /home/pi/exhibit-player.py
	chmod +x /home/pi/Start-exhibit-player.sh
```
- Format a USB flash drive, giving it the volume label `USBDISK`.
- Create the directory `Videos` on the flash drive.
- Copy the video files to the `Videos` directory on the flash drive. Name the files so that they appear in the desired order when you list them with `ls -1 /media/pi/USBDISK/Videos/` from the RPi. Remember that the first file will be used as the default video.
- Insert the following code into `/etc/rc.local` before the `exit 0` to start the script at system boot:
```bash
	sudo /home/pi/Start-exhibit-player.sh &
```
- Shutdown the Raspberry Pi.
- Connect the switches to the GPIO pins.
- Apply power to the Raspberry Pi.

## GPIO mapping

The script uses five GPIO pins (3, 7, 11, 13, 15). When tied to ground (pins
6, 9, 14, 20, 25, 30, 34, 39), the associated video begins playing.

Pin | GPIO | Function
----|------|---------
3 | GPIO2 | When held low for two seconds, execute `sudo poweroff`
7 | GPIO4 | Play video 1
11 | GPIO17 | Play video 2
13 | GPIO27 | Play video 3
15 | GPIO22 | Play video 4

## Notes

- The path to the video file storage is set near the top of the script. Look for the variable `videodir`. The USB flash drive can be eliminated by storing the videos on the microSD card (e.g., in `/home/pi/Videos`). We believe our museum staff will be more successful copying files to a familiar, VFAT-formatted USB flash drive using almost any computer (Windows, Mac, Linux) than they would with a tiny microSD card containing a ext4-formatted file system on a PC running Linux.
- The USB flash disk volume name can be changed. Remember to change `videodir` in `exhibit-player.py`, the startup script (Start-exhibit-player.sh), and adjust the installation instructions as appropriate.
- Recommended: Restrict file names to use characters a-z, A-Z, 0-9, underscore, hyphen, and period. No testing has been done with file names containing special characters or spaces.
- Recommended: Restrict USB flash drive volume names to use characters a-z, A-Z, and 0-9.
- Additional buttons can be added with relatively simple changes to the script.

## References

- [Raspberry Pi Getting Started Guide](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
- [Raspberry Pi 3B+ Product Brief](https://static.raspberrypi.org/files/product-briefs/Raspberry-Pi-Model-Bplus-Product-Brief.pdf)
- [Raspberry Pi GPIO Usage](https://www.raspberrypi.org/documentation/usage/gpio/)

