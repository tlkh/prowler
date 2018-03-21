import cProfile, pstats, io
pr = cProfile.Profile()
pr.enable()

hostname = "172.22.0.166"

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
            uid_list=["pi","odroid","root","admin"]
            pwd_list=["raspberry","odroid","root","admin","password"]
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
#return (hostname, valid)



pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
