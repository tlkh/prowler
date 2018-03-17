# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 10:41:03 2017

@author: faith
"""

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

# start a new nmap scan on localhost with some specific options
def do_scan(host, options):
    # uncomment line below to manually input target IP
    #host = input("Enter Target Host Address: ")
    parsed = None
    nmproc = NmapProcess(host, options)
    rc = nmproc.run()
    if rc != 0:
        print("nmap scan failed: {0}".format(nmproc.stderr))
    print(type(nmproc.stdout))

    try:
        parsed = NmapParser.parse(nmproc.stdout)
    except NmapParserException as e:
        print("Exception raised while parsing scan: {0}".format(e.msg))

    return parsed

if __name__ == "__main__":
    #change IP address below to target IP to immediately run upon execution
    report = do_scan("172.22.0.166", "-sV")
    if report:
        print_scan(report)
    else:
        print("No results returned")

# print scan results from a nmap report
def print_scan(nmap_report):
    print("Starting Nmap {0} ( http://nmap.org ) at {1}".format(
        nmap_report.version,
        nmap_report.started))
    print ("=" * 60)

    for host in nmap_report.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        print("Nmap scan report for {0} ({1})".format(
            tmp_host,
            host.address))
        print("Host is {0}.".format(host.status))
        print ("-" * 60)
        print("    PORT   STATE         SERVICE")
        for serv in host.services:
            pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(
                    str(serv.port),
                    serv.protocol,
                    serv.state,
                    serv.service)
            if len(serv.banner):
                pserv += " ({0})".format(serv.banner)
            print(pserv)
        print ("=" * 60)
    print("Summary: ", nmap_report.summary)