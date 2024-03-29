import json
import os
import sys
import time

import pika

from models import Contact


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    queue_name = 'web_16_campaign'
    channel.queue_declare(queue=queue_name, durable=True)

    consumer = "GoIT_web16_mod8_task2"

    def callback(ch, method, properties, body):
        pk = body.decode()
        task = Contact.objects(id=pk, message_sent=False).first()
        if task:
            task.update(set__message_sent=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Task completed: {task.fullname}, {task.email}, {task.id}")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
