import logging, pika, sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

def setup_message_queue(topic):
        """Setup RabbitMQ messaging system"""
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=topic)
        channel.exchange_declare(exchange=topic+"_exchange",
                                 exchange_type='topic')
        print("[i] Running: message queue on: " + topic)
        return True

def publish(topic, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.basic_publish(exchange=topic+"_exchange",
                      routing_key=topic,
                      body=message)
        print("[T] Sent message: " + message)
        return True

def read_packet(pkt):
        if pkt.haslayer(IP): # If our packet has an IP layer
            ip_address = pkt[IP].src # get IP address (located in IP layer)
            MACaddress = pkt[Ether].src # get MAC address (located in Ether Layer)

            if ip_address not in address_list:
                address_list.append(ip_address)
                print('\n[+] ' + str(pkt.summary()))
                print('[+] Host Found\n[i] MAC: ' + MACaddress + ' | IP: '+ ip_address)
                publish("ip_address", ip_address)
                
def list(address_list): 
    return read_packet

setup_message_queue("ip_address")
address_list = []

try:
        print('[i] Listening... \n')
        sniff(prn=list(address_list)) # Sniff any type of packet, send each of them to readPacket()
except Exception as e:
        print("\n[!] Error: " + str(e))
        print("[i] Exiting...")
        pass
