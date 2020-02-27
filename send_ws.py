#!/usr/bin/env python
import pika

import json
import uuid

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

my_func={
        'func': 'guillotina_notification.task.post_new_notification_wsocket',
        'args': ['Bob123', 'Bob messaggio in pipe e ws', 'Django-freeman'],
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
                        #faccio un test con gli headers sbagliati, idealmente qui ci sarà Django come user-agent(?)
                        #'User-Agent': 'python-requests/2.22.0',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept': '*/*',
                        'Connection': 'keep-alive'
                }
        }
}

#lo trasformo in una stringa Json con la 'dumbs'

channel.publish(exchange='guillotina', routing_key='guillotina', body=json.dumps(my_func))
print(" [x] Sent 'Hello World!'")

connection.close()
