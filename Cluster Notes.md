# Simple Python Cluster

## Hardware
- Raspberry Pi HAT (4 * Pi Zero W)
- Raspberry Pi 3
- No external router needed!

## Software
- Python 3.6
- Dispy
- [pssh](https://www.tecmint.com/execute-commands-on-multiple-linux-servers-using-pssh/)

## Important Code
- To run ssh command on multiple devices `pssh -h pssh-hosts -l username -A -i "command"`
- To create the cluster (in octopi/`compute.py`): `cluster = dispy.JobCluster(compute, nodes='pi0_ip', ip_addr='pi3_ip')`
- Check connectivity: `ping p1.local -c 1 && ping p2.local -c 1 && ping p3.local -c 1 && ping p4.local -c 1`