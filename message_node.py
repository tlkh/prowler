import pika
import sys

class ResultsStream:
    """Seperate thread to continously process incoming messages"""
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='scan_results',
                                exchange_type='topic')

        self.result = self.channel.queue_declare(exclusive=True)
        self.queue_name = self.result.method.queue

        self.channel.queue_bind(exchange='scan_results_exchange',
                        queue=self.queue_name,
                        routing_key='scan_results')

        print("[i][Pika] Configured connections")

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        print("[+][Pika] Watching channel (blocking!)")
        self.channel.basic_consume(self.callback, queue=queue_name, no_ack=True)
        self.channel.start_consuming()

    def callback(ch, method, properties, message_body):
        """Callback function to process message"""
        print("\n[R] %r:%r" % (method.routing_key, message_body))
        message = str(message_body)
        print(message)

stream = ResultsStream()
stream.start()


