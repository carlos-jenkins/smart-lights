#!/usr/bin/env bash

# Locales config
sudo apt-get install locales
sudo dpkg-reconfigure locales
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8

# Basic tools
sudo apt-get install ca-certificates tree git

# Python environment
sudo apt-get install python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py
sudo pip3 install tox webdev

# I2C
sudo apt-get install build-essential i2c-tools libi2c-dev libffi-dev python3-dev python3-numpy
sudo pip3 install smbus-cffi
# sudo adduser chip i2c
# Execute: sudo i2cdetect -y 0/2
# Check: ls /dev/i2c*
