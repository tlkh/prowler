import pika
import sys

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser
import libnmap.objects.os as NmapOS

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='ip_address_exchange',
                         exchange_type='topic')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='ip_address_exchange',
                   queue=queue_name,
                   routing_key='ip_address')

print('[i] Waiting for IP addresses. To exit press CTRL+C')

def check_hostname(hostname):
    nmproc = NmapProcess(hostname, "-sV")
    rc = nmproc.run()
    parsed = NmapParser.parse(nmproc.stdout)
    host = parsed.hosts[0]

    return host, host.services, host.os

def callback(ch, method, properties, message_body):
    print("\n[R] %r:%r" % (method.routing_key, message_body))
    hostname = str(message_body)[2:].replace("'","")
    print("[i] Checking hostname " + hostname)
    print(check_hostname(hostname))
    

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

try:
    channel.start_consuming()
except Exception as e:
    print("\n[!] Error: " + str(e))
    print("[i] Exiting...")
    pass
