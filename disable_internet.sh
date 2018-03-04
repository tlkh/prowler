#!/usr/bin/env bash

echo "Current Wireless Capabilities:"
sudo rfkill list all

echo "Disabling Wifi and enabling ethernet"
sudo ifconfig wlan0 down
sudo rfkill block 0
sudo ifconfig br0 up
sudo ifconfig enxb827eb7ae466 up

echo "Internet enabled:"
sudo rfkill list all

echo "IP addresses:"
sudo ifconfig | grep inet
