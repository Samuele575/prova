from guillotina import task_vars as g_task_vars
from guillotina.utils import get_current_request

from guillotina_amqp import task

import time
from datetime import datetime

import json
import random
import requests

'''
decido per ora di passare 3 parametri:
not_type----------->usato per indicare il tipo di notifica

recipientId-------->lo userId che userò per cercare la socket
                fra quelle aperte e per poterle tracciare dopo, vedremo poi se sia possibile o meno

email_recipient---->email per l'invio se si chima la send_mail

message------------>la notifica che dovrò inviare, la gestisco come Text

subject------------>Il titolo utile alle email

app---------------->il nome della applicazione che uso come Folder per salvare le notifiche di ogni utente

status------------->non inviato, ma usato, uso 2 stati fissi
                    NOT_NOTIFIED
                    NOTIFIED
'''

@task
async def post_new_notification(not_type, recipientId, email, message, app, not_time):

    #import pdb; pdb.set_trace()
    s = time.perf_counter()

    subject = ("Notification to " + recipientId)

    random_id = ('Notify_to_' + recipientId + '_' + str(len(message)+random.randint(0,1000)) + '_' + str(len(recipientId)+random.randint(0,1000)) + '_' + str(len(app)+random.randint(0,1000)))

    task_request = get_current_request()

    #format = '%Y-%m-%dT%H:%M:%S.%f+00:00' # The format 
    #datetime_str = datetime.strptime(not_time, format)

    requests.post(
        str(task_request.url), 
        headers= { 'Accept': 'application/json', 'Content-Type': 'application/json', },
        json={ 
            '@type': 'Notification', 
            'id': random_id, 
            'not_type': not_type, 
            'recipientId': recipientId,
            'email_recipient': email, 
            'subject': subject,
            'message': message,
            'application_name': app,
            'notification_date': not_time,
            'status': 'NOT_NOTIFIED', }, 
        auth=('root', 'root'))

    print(task_request.url)

    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")