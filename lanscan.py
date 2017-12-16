# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 15:43:05 2017

@author: faith
"""

#!/usr/bin/python

import os
from netaddr import *
import argparse
import subprocess
import socket
from sys import argv
import datetime
from prettytable import PrettyTable
from progressbar import Bar, Percentage, ProgressBar, ETA, SimpleProgress
import progressbar
# DNS Lookup
def lookup(addr):
    try:
        return socket.gethostbyaddr(str(addr))
    except:
        return None, None, None

# Parsing the Arguments
parser = argparse.ArgumentParser(description='LAN-SCAN')
parser.add_argument('-n','--network', help='e.g. 192.168.10.0/24', required=True)
parser.add_argument('-d','--dns', help='FALSE sets DNS lookup active or inactive')
parser.add_argument('-l','--log', help='TRUE creates a comma-seperated-logfile')
parser.add_argument('-o','--online', default='True', help='show only online hosts')

args = vars(parser.parse_args())
network = str(args['network'])
dns = str(args['dns'])
online = str(args['online'])

log = str(args['log'])
if (log==None):
    logging=False
elif ((log=="True") or (log=="TRUE") or (log=="true")):
    logging=True
elif ((log=="False") or (log=="FALSE") or (log=="false")):
    logging=False
else:
    logging=False

# Check if DNS Lookup-Argument is set
if(dns==None):
    nslookup=True
elif((dns=="True") or (dns=="true") or (dns=="TRUE")):
    nslookup=True
elif((dns=="False") or (dns=="FALSE") or (dns=="false")):
    nslookup=False
else:
    nslookup=True

# Check-Loop
print ("\n** Scanning "+network+" for hosts **\n")

#print ("IP\t\tStatus\tName")
#print ("--\t\t--\t--")
x = PrettyTable(["IP Address", "Status", "Name"])
x.align["IP Address"] = "l" 
x.align["Name"] ="l"
x.padding_width = 1
count = 0
hostssalive =""
ips = 0

#logging
ts= str(datetime.date.today())

if (logging==True):
    fw = open('ipscan_'+ts+'.csv','w')
    fw.write("IP,Status,Name\n")

pbar = ProgressBar(widgets=[Percentage(), Bar(), ETA()], maxval=len(IPSet([network]))).start()

for ip in  IPSet([network]):
    try:
        response = subprocess.check_output(
        ["ping", "-c", "1", "-n", "-W", "1", "-i","0.1", str(ip)],
        stderr=subprocess.STDOUT,
        universal_newlines=True)

        if (nslookup):
            name,alias,addresslist = lookup(ip)
            if (name==None):
                name = ""
        else:
            name = ""
        #print (str(ip)+"\tALIVE\t"+name)
        x.add_row([str(ip),"ONLINE",name])
        if (logging==True):
            fw.write(str(ip)+",ALIVE,"+name+"\n")

        count += 1
        if (name != ""):
            hostssalive += str(ip)+"\t"+name+"\n"
        else:
            hostssalive += str(ip)+"\n"

    except subprocess.CalledProcessError:
        response = None
        if (online!="True"):
           # print (str(ip))
            x.add_row([str(ip),"OFFLINE",""])
            if (logging==True):
                fw.write((str(ip)+"\n"))
   # r.update(ips)
    pbar.update(ips)
    ips=ips+1
pbar.finish()
print ("\n")
print (x)


print ("\n")# Summary
#print ("\nSummary\n--\n"+str(ips)+" IP's scanned")
y = PrettyTable(["IPs scanned", "IPs alive"])
y.align["IPs scanned"] = "l" # Left align city names
y.align["IPs alive"] = "l" # Left align city names
y.padding_width = 1

y.add_row([str(ips), str(count)])
print (y)
#
#if (int(count) == 1):
#    print (str(count)+" host alive")
#else:
#    print (str(count)+" hosts alive")
#if (online!="True"):
#    if (hostssalive != ""):
#        print ("\n"+hostssalive)
#    else:
#        print ("")
print ("\n")