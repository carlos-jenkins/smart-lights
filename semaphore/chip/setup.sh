#!/usr/bin/env bash

sudo apt-get install locales
sudo dpkg-reconfigure locales
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8
sudo apt-get install python3 ca-certificates tree git
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py
sudo pip3 install tox webdev
