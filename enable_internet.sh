#!/usr/bin/env bash

echo "Current Wireless Capabilities:"
sudo rfkill list all

echo "Enabling Wifi and disabling ethernet"
sudo rfkill unblock 0
sudo ifconfig br0 down
sudo ifconfig enxb827eb7ae466 down
sudo ifconfig wlan0 up

echo "Internet enabled:"
sudo rfkill list all

echo "IP addresses:"
sudo ifconfig | grep inet
