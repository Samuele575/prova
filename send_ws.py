#!/usr/bin/env python3
# countsync.py

import time
from datetime import datetime

import pika
import json
import uuid

def main(*args):
    notification_type = args[0]
    recipient_ID = args[1]
    recipient_email = args[2]
    notification_subject = args[3]
    application_name = args[4]

    #open the connection with the rabbitMQ exchange
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    
    i = datetime.now()
    notification_time = i.strftime("%Y-%m-%dT%H:%M:%S.%f+00:00")
    #prepare the message's body, using args
    my_func={
            'func': 'guillotina_notification.task.post_new_notification',
            'args': [notification_type, recipient_ID, recipient_email, notification_subject, application_name, notification_time],
            'kwargs': {},

            'user': 'root',

            'db_id': 'db',
            'container_id': 'container',

            'task_id': str(uuid.uuid4()),

            'annotations': {},

            'req_data': {
                    'url': 'http://localhost:8080/db/container',
                    'method': 'POST',

                    'headers': {
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept': '*/*',
                            'Connection': 'keep-alive'
                    }
            }
    }

    #using the 'dumbs' function to translate the 'my_func' object in JSON 

    channel.publish(exchange='guillotina', routing_key='guillotina', body=json.dumps(my_func))
    print(" [x] Sent 'Hello World!'")

    connection.close()

if __name__ == "__main__":
    import sys
    s = time.perf_counter()
    args = ['SIMPLE', 'Bob123', 'bob@foobar.it', 'Ciao Bob inviato da Bim', 'Django'] if len(sys.argv) == 1 else map(int, sys.argv[1:])
    main(*args)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
