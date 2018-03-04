#!/usr/bin/env bash

echo "Updating device..."
sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove && sudo apt clean

echo "Configuring environment..."
sudo apt install python3-dev python3-pip python3-numpy
sudo apt install nmap
sudo pip3 install setuptools wheel pip --upgrade
sudo pip3 install -r requirements.txt
