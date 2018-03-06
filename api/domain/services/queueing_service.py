import pika


class QueueingService:
    def __init__(self):
        pass

    def enqueue(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue', port=5672))
        channel = connection.channel()
        channel.queue_declare(queue='train')
        channel.basic_publish(exchange='',
                              routing_key='train',
                              body='train')
        print(" [x] Sent request to queue")
        connection.close()