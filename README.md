# Wave converter for Akai MPC and Roland SP
Simple Wave Converter using ffmpeg to 44000 with tk gui.
Mainly coded for use in Linux. 

I have no idea if it can be run in Windows.

## Dependencies:

- _tk_
- _ffmpeg_

Make sure you have ffmpeg installed and available to your PATH.
Install TK to your system.


For Windows:
Download the ffmpeg executable from the official website.
Extract the downloaded zip file to a directory (e.g., C:\ffmpeg).
Open the Start Menu, search for "Environment Variables," and select "Edit the system environment variables."
In the System Properties window, click the "Environment Variables" button.
In the Environment Variables window, find the "Path" variable in the "System variables" section and select it. Click "Edit."
Click "New" and add the path to the ffmpeg bin directory (e.g., C:\ffmpeg\bin).
Click "OK" to close all windows.

For macOS:
Install ffmpeg using Homebrew (if you don't have Homebrew, install it first from brew.sh):
sh brew install ffmpeg


For Linux:
Install ffmpeg using your package manager:
Debian/Ubuntu:
sudo apt update
sudo apt install ffmpeg

CentOS/RHEL:
sudo yum install epel-release
sudo yum install ffmpeg

Arch Linux:
Sudo pacman -S ffmpeg
