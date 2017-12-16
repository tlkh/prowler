def compute(hostname):
    import os
    response = os.system("ping -c 1 -w 1 " + hostname)
    if response == 0:
      valid = "alive"
      #then perform port scanning
      ports = ["20","8888"]
      types = ["camera", "fridge"]
      import pyrebase
      config = {
          "apiKey": "AIzaSyCOhJuPsdThHoPghb3LxwVJv9WJVyRIYms",
          "authDomain": "clusterscanner.firebaseio.com",
          "databaseURL": "https://clusterscanner.firebaseio.com/",
          "storageBucket": "clusterscanner.appspot.com"
        }
      firebase = pyrebase.initialize_app(config)
      auth = firebase.auth()
      user = auth.sign_in_with_email_and_password("pi@cluster.pi", "asdf1234")
      db = firebase.database() # reference to the database service
      hoststruct = hostname.split(".")
      data = {"hostname": hostname,
              "ports": ports,
              "device_type": types}
      results = db.child(hoststruct[0]).child(hoststruct[1]).child(hoststruct[2]).child(hoststruct[3]).set(data, user['idToken'])
    else:
      valid = "dead"
    return (hostname, valid)

if __name__ == '__main__':
    import dispy
    import dispy.httpd
    import time
    
    workers = ['169.254.102.163','169.254.116.199','169.254.114.226','169.254.156.34']

    auto_ssh = False

    cluster = dispy.JobCluster(compute, nodes=workers, ip_addr='169.254.148.126')
    http_server = dispy.httpd.DispyHTTPServer(cluster)

    jobs = []
    test_range = []
    for i in range (0,1):
        for j in range (0,255):
            test_range.append("172.22."+str(i)+"."+str(j))
    print("Testing "+str(len(test_range))+" hostnames")

    time.sleep(4)
    cluster.print_status()

    start = time.time()

    for i, address in enumerate(test_range):
        # schedule execution of 'compute' on a node (running 'dispynode')
        # with a parameter (random number in this case)
        job = cluster.submit(address)
        job.id = i # optionally associate an ID to job (if needed later)
        jobs.append(job)
    # cluster.wait() # waits for all scheduled jobs to finish

    '''if auto_ssh == True:
        print("Starting nodes...")
        import paramiko
        for worker in workers:
            print("Starting node on " + str(worker))
            client = paramiko.client.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy)
            client.connect(worker,port=22, username="pi", password="asdf1234")
            stdin, stdout, stderr = client.exec_command('nohup ./start.sh')
            client.close()
            print(worker + " started.")'''
    
    for job in jobs:
        hostname, valid = job() # waits for job to finish and returns results
        print(job.ip_addr+": "+hostname+" is "+valid+".")
        # other fields of 'job' that may be useful:
        # print(job.stdout, job.stderr, job.exception, job.ip_addr, job.start_time, job.end_time)
        
    end = time.time()
    cluster.print_status()
    http_server.shutdown()
    cluster.close()

    print("")
    print("Total time taken = " + str(end-start))
