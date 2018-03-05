def compute(hostname):
    import os
    if (os.system("ping -c 1 -w 1 " + hostname)) == 0:
        valid = "alive"
        from libnmap.process import NmapProcess
        from libnmap.parser import NmapParser
        nmproc = NmapProcess(hostname, "-sV")
        rc = nmproc.run()
        parsed = NmapParser.parse(nmproc.stdout)
        host = parsed.hosts[0]
        services = []
        status = "Unknown"
        cracked = False
        for serv in host.services:
            services.append(str(serv.port) + "/" + str(serv.service))
            if serv.port == 22:
                import paramiko
                client = paramiko.client.SSHClient()
                client.load_system_host_keys()
                client.set_missing_host_key_policy(paramiko.WarningPolicy)
                splitted=[]
	            f=open('wordlist 1.txt','r')
	            for i in f.readline().split(' '):
	            	if bool(i)==True:
	            		splitted.append(i)
	            uid_list=[]
	            pwd_list=[]
	            for i in range(len(splitted)):
	            	if i==0 or i%2==0:
	            		uid_list.append(i)
	            	else:
	            		pwd_list.append(i)
	            for uid in uid_list:
                    for pwd in pwd_list:
                        try:
                            if cracked == False:
                                client.connect(hostname,username=uid,password=pwd)
                                stdin, stdout, stderr = client.exec_command('ls -l')
                                status = "Poor SSH Credentials"
                                print("PWNNEEDDDD!!!!")
                                cracked = True
                        except:
                            print("failed to pwn")
                            status = "Unknown"
                client.close()
        import pyrebase
        config = {
            "apiKey": "",
            "authDomain": "clusterscanner.firebaseio.com",
            "databaseURL": "https://clusterscanner.firebaseio.com/",
            "storageBucket": "clusterscanner.appspot.com"
        }
        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password("pi@cluster.pi", "")
        db = firebase.database()  # reference to the database service
        hoststruct = hostname.split(".")
        data = {"hostname": hostname,
                "services": services,
                "status": status}
        results = db.child(hoststruct[0]).child(hoststruct[1]).child(
            hoststruct[2]).child(hoststruct[3]).set(data, user['idToken'])
    else:
        valid = "dead"
    return (hostname, valid)


if __name__ == '__main__':
    import dispy
    import dispy.httpd
    import time

    workers = ['169.254.102.163', '169.254.116.199',
               '169.254.114.226', '169.254.156.34']

    cluster = dispy.JobCluster(
        compute, nodes=workers, ip_addr='169.254.148.126')
    http_server = dispy.httpd.DispyHTTPServer(cluster)

    jobs = []
    test_range = []
    for i in range(0, 1):
        for j in range(100, 200):
            test_range.append("172.22." + str(i) + "." + str(j))
    print("Testing " + str(len(test_range)) + " hostnames")

    time.sleep(4)
    cluster.print_status()

    start = time.time()

    for i, address in enumerate(test_range):
        # schedule execution of 'compute' on a node (running 'dispynode')
        # with a parameter (random number in this case)
        job = cluster.submit(address)
        job.id = i  # optionally associate an ID to job (if needed later)
        jobs.append(job)
    # cluster.wait() # waits for all scheduled jobs to finish

    for job in jobs:
        try:
            hostname, valid = job()  # waits for job to finish and returns results
            print(job.ip_addr + ": " + hostname + " is " + valid + ".")
            # other fields of 'job' that may be useful:
            # print(job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time)
        except Exception as e:
            print(str(job) + " failed: " + str(e))

    end = time.time()
    cluster.print_status()
    http_server.shutdown()
    cluster.close()

    print("")
    print("Total time taken = " + str(end - start))
