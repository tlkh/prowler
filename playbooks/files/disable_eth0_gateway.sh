#!/usr/bin/env bash

ip4=$(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)

sudo echo "interface eth0" >> /etc/dhcpcd.conf
sudo echo "static ip_address=$ip4" >> /etc/dhcpcd.conf
sudo echo "nogateway" >> /etc/dhcpcd.conf