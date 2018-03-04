#!/usr/bin/env bash

sudo apt update
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt autoremove

sudo apt install python3-dev python3-pip python3-numpy
sudo apt install nmap
sudo pip3 install setuptools wheel pip --upgrade
sudo pip3 install -r requirements.txt