import cProfile, pstats, io
pr = cProfile.Profile()
pr.enable()
import os
hostname = "172.22.0.166"
if (os.system("ping -c 1 -w 1 " + hostname)) == 0:
    valid = "alive"
    from libnmap.process import NmapProcess
    from libnmap.parser import NmapParser, NmapParserException
    hostname = "172.22.0.166"
    nmproc = NmapProcess(hostname, "-sV")
    rc = nmproc.run()
    parsed = NmapParser.parse(nmproc.stdout)
    host = parsed.hosts[0]
    services = []
    for serv in host.services:
        services.append(str(serv.port) + "/" + str(serv.service))
    import pyrebase
    config = {
        "apiKey": "AIzaSyCOhJuPsdThHoPghb3LxwVJv9WJVyRIYms",
        "authDomain": "clusterscanner.firebaseio.com",
        "databaseURL": "https://clusterscanner.firebaseio.com/",
        "storageBucket": "clusterscanner.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password(
        "pi@cluster.pi", "asdf1234")
    db = firebase.database()  # reference to the database service
    hoststruct = hostname.split(".")
    data = {"hostname": hostname,
            "services": services}
    results = db.child(hoststruct[0]).child(hoststruct[1]).child(
        hoststruct[2]).child(hoststruct[3]).set(data, user['idToken'])
else:
    valid = "dead"
pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
