import os
import dispy

test_range = []

for i in range (0,1):
    for j in range (0,256):
        test_range.append("172.22."+str(i)+"."+str(j))

def test_ip(hostname):
    response = os.system("ping -c 1 -W 400 " + hostname)
    if response == 0:
      print(hostname+str(" valid"))
    else:
      print(hostname+str(" not valid"))

cluster = dispy.JobCluster(test_ip, nodes=['worker1', '169.254.102.163', 'worker2', '169.254.116.199', 'worker3', '169.254.114.226', 'worker4', '169.254.156.34',]

jobs = []

for i, address in enumerate(test_range):
    job = cluster.submit(address)
    job.id = i
    jobs.append(job)

for job in jobs:
    host, n = job()
    print('%s executed job %s at %s with %s' % (host, job.id, job.start_time, n))
    cluster.print_status()