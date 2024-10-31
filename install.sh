#!/bin/bash

echo "Installing required packages for SOVSPAM..."
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install pyautogui keyboard
echo "Installation complete! You can now run SOVSPAM."
