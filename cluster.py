def compute(hostname):
    import os
    valid = "online"
    breached = False
    credentials = None
    fingerprint = None
    services = None
    os_match = None
    if (os.system("ping -c 1 -w 1 " + hostname)) == 0:
        print("Host", hostname, "is online, starting nmap")
        from libnmap.process import NmapProcess
        from libnmap.parser import NmapParser
        from libnmap.objects.os import NmapOSClass
        nmproc = NmapProcess(targets=hostname, options="-O")
        rc=nmproc.run()
        parsed = NmapParser.parse(nmproc.stdout)
        host = parsed.hosts[0]
        #print("{0} {1}".format(host.address, " ".join(host.hostnames)))
        os_match = []
        if host.os_fingerprinted:
            fingerprint = host.os.osmatches
            print("OS Fingerprint:")
            for osm in host.os.osmatches:
                print("Found Match:{0} ({1}%)".format(osm.name, osm.accuracy))
                for osc in osm.osclasses:
                    os_match.append(str(osc.description))
                    print("\tOS Class: {0}".format(osc.description))
        else:
            fingerprint = None
        services = []
        for serv in host.services:
            services.append(str(serv.port) + "/" + str(serv.service))
            print("Open ports:", services)
            if serv.port == 22:
                print("------starting credentials test------")
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
                        if breached == False:
                            #time.sleep(0.1) # for when SSH connection keeps dropping
                            try:
                                client.connect(hostname,username=uid,password=pwd)
                                stdin, stdout, stderr = client.exec_command('ls -l')
                                print("[!] Successfully connected to host", hostname)
                                status = "Poor SSH Credentials"
                                breached = True
                                credentials = [uid, pwd]
                                client.close()
                            except paramiko.AuthenticationException:
                                client.close()
                                #print("Failed to pwn. Trying again...")
                            except Exception as e:
                                print("Failed to pwn, error:", e)
                    except Exception as e:
                        print("Failed to pwn, error:", e)
    else:
        valid = "offline"
    return hostname, os_match, services, breached, valid

if __name__ == '__main__':
    import dispy, time, pika
    import logging
    import dispy.httpd

    print("[i][dispy] Initialising Cluster")

    #workers = ['192.168.0.133','192.168.0.110'
    workers = ['192.168.0.170','192.168.0.111',
               '192.168.0.153','192.168.0.195']

    cluster = dispy.JobCluster(compute, nodes=workers, ip_addr='192.168.0.142')
    http_server = dispy.httpd.DispyHTTPServer(cluster)

    jobs, test_range = [], []

    for i in range(0, 1):
        for j in range(0, 255):
            test_range.append("192.168." + str(i) + "." + str(j))

    print("[i] Testing " + str(len(test_range)) + " hostnames")

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='scan_results')

    time.sleep(4) # make sure cluster is connected
    cluster.print_status()

    start = time.time()

    for i, address in enumerate(test_range):
        # schedule execution of 'compute' on a node (running 'dispynode.py') with a parameter
        job = cluster.submit(address)
        job.id = i  # optionally associate an ID to job (if needed later)
        jobs.append(job)
    # cluster.wait() # waits for all scheduled jobs to finish

    for job in jobs:
        try:
            result = job()
            hostname, fingerprint, services, breached, valid = result  # waits for job to finish and returns results
            #result_security = str(hostname) + " is " + str(valid) + ". Breached: " str(breached) + " with credentials " + str(credentials)
            #print(job.ip_addr,":",result_security)
            #print(os_matches)
            if valid == "online":
                message = [hostname, fingerprint, services, breached]
                print(message)
                try:
                    channel.basic_publish(exchange='scan_results_exchange', routing_key='scan_results', body=str(message))
                    print("Message published")
                except Exception as e:
                    print("[!] Message failed to publish:", str(e))
                    try:
                        print("Refreshing connection")
                        try:
                            connection.close()
                        except Exception as e:
                            print(e)
                            pass
                        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
                        channel = connection.channel()
                        channel.queue_declare(queue='scan_results')
                    except Exception as e:
                        print("Error restarting connection", str(e))
                    channel.basic_publish(exchange='scan_results_exchange', routing_key='scan_results', body=str(message))
                    print("Message published successfully (second time)")
                # print('OS Description : {0}'.format(osclass['osfamily']) for osclass in nmap.Portscanner[job.ip_addr]['osclass'])
                # other fields of 'job' that may be useful:
                # print(job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time)
            else:
                print(hostname, "is offline")
        except Exception as e:
            print("[!]",str(job),"failed with error:",str(e))
            print("[+] Debug:", job.stdout, job.stderr, job.exception)

    connection.close()

    end = time.time()
    print("\n","[i] Total time taken =", str(end - start))
    cluster.print_status()
    http_server.shutdown()
    cluster.close()
