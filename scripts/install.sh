#!/bin/bash

# Destination directory for the launch_KlipperScreen.sh file
destination_directory="/home/pi/KlipperScreen/scripts/"

# Content of the launch_KlipperScreen.sh file
script_content="# Launch Updater
/usr/bin/xinit /home/pi/.KlipperScreen-env/bin/python /home/pi/GingerUpdater/screen.py

# After updater Launch KlipperScreen
/usr/bin/xinit /home/pi/.KlipperScreen-env/bin/python /home/pi/KlipperScreen/screen.py
"

# Create the file in the specified directory
echo "$script_content" > "$destination_directory/launch_KlipperScreen.sh"

# Set execution permissions for the file
chmod +x "$destination_directory/launch_KlipperScreen.sh"

echo "File launch_KlipperScreen.sh created successfully in $destination_directory"
