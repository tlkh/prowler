# Pi Vulnerability Scanner Cluster
### Infosec Community Hackathon 2017

## Hardware
- Raspberry Pi HAT (4 * Pi Zero W)
- Raspberry Pi 3
- No external router needed!

## Software
- Python 3.6
- Dispy
- [pssh](https://www.tecmint.com/execute-commands-on-multiple-linux-servers-using-pssh/)

## Important Snippets
- To run ssh command on multiple devices `pssh -h pssh-hosts -l username -A -i "command"`
- To create the cluster (in octopi/`compute.py`): `cluster = dispy.JobCluster(compute, nodes='pi0_ip', ip_addr='pi3_ip')`
- Check connectivity: `ping p1.local -c 1 && ping p2.local -c 1 && ping p3.local -c 1 && ping p4.local -c 1`
- Temperature Check: `/opt/vc/bin/vcgencmd measure_temp && pssh -h workers -l pi -A -i "/opt/vc/bin/vcgencmd measure_temp" | grep temp`

## Files
- `compute.py` is the main file

## Other random stuff:
https://sonar.labs.rapid7.com/
http://resources.infosecinstitute.com/popular-tools-for-brute-force-attacks/
https://nmap.org/
https://pypi.python.org/pypi/python-nmap
https://docs.python.org/3.6/library/subprocess.html#module-subprocess
http://qdosmsq.dunbar-it.co.uk/blog/2013/03/linux-command-to-retrieve-hardware-serial-numbers-etc/
https://github.com/jeanphorn/wordlist

