#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "Warning: not root"
fi

USE_APT=1
command -v apt-get >/dev/null 2>&1 || USE_APT=0

if [ "$USE_APT" -ne "0" ]; then
    echo "Found apt command. Installing apt packages..."
    apt-get install python3
    apt-get install pip3
    apt-get install mp3info
else
    echo "Did not find apt command. Make sure you install the necessary packages."
fi

echo "Installing pip3 packages..."
pip3 install bs4
