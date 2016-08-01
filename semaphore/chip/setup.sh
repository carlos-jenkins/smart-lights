#!/usr/bin/env bash
set -o errexit
set -o nounset

# Locales config
sudo apt-get install locales
sudo dpkg-reconfigure locales
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8

# Basic tools
sudo apt-get install -y ca-certificates tree git

# Python environment
sudo apt-get install -y python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py
sudo pip3 install tox webdev

# I2C
sudo apt-get install -y build-essential i2c-tools libi2c-dev libffi-dev python3-dev
sudo pip3 install smbus-cffi
# sudo adduser chip i2c
# Execute: sudo i2cdetect -y 0/2
# Check: ls /dev/i2c*

# User configuration
# Add to .bashrc:
# alias la='ls -lah'
# export PATH=/usr/sbin:$PATH
