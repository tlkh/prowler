import paramiko
client = paramiko.client.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.WarningPolicy)
try:
  client.connect('172.22.0.166',username='pi',password='raspberry')
  stdin, stdout, stderr = client.exec_command('ls -l')
except (paramiko.ssh_exception.AuthenticationException):
  print('LOLOL try harder') 

