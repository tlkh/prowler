#import paramiko
import os

client = paramiko.client.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.WarningPolicy)

def test_rpi(hostname):
    try:
        client.connect(str(hostname),port=22, username="pi", password="raspberry")
        stdin, stdout, stderr = client.exec_command('ls -l')
        #print(stdout.readlines())
        print("[!!!]: " + hostname)
        print("Default password found (Raspberry Pi)")
    except Exception as e:
        print(hostname + " error: " + str(e))

test_range = []

for i in range (0,1):
    for j in range (0,256):
        test_range.append("172.22."+str(i)+"."+str(j))

print(test_range)

for address in test_range:
    print("")
    print("")
    print("testing " + str(address))
    hostname = address #example
    response = os.system("ping -c 1 -W 400 " + hostname)
    if response == 0:
      print(hostname+str(" valid"))
    else:
      print(hostname+str(" not valid"))
