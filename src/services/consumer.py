import functools
import pika
import os

import sys
sys.stdout = open('/app/newoutput.txt', 'w')


def process_message(chan, method_frame, _header_frame, body, userdata=None):
    chan.basic_ack(delivery_tag=method_frame.delivery_tag)

    print('got to process message', body, flush=True)


def main():
    conn_params = pika.URLParameters(os.environ['AMQP_URI'])
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    channel.queue_declare(queue='photo_processor', durable=True, auto_delete=False)

    on_message_callback = functools.partial(
        process_message, userdata='on_message_userdata')
    channel.basic_consume('photo_processor', on_message_callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()


if __name__ == '__main__':
    main()
