import pika
from pika.exceptions import ConnectionClosed
import time

from domain.services.callback_service import CallbackService


def main():
    callback_service = CallbackService()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='queue', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='train')
    channel.basic_consume(callback_service.callback,
                          queue='train',
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    while(True):
        try:
            main()
        except ConnectionClosed:
            sleep_time = 30
            print('could not connect. waiting for', sleep_time, 'seconds...')
            time.sleep(sleep_time)


