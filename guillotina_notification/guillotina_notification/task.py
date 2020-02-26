from guillotina import task_vars as g_task_vars

from guillotina.component import get_utility #getUtilty
from guillotina.content import create_content_in_container

from guillotina_notification.content import INotification
from guillotina.utils import get_current_request, get_current_container
from guillotina.interfaces import IRolePermissionManager

from guillotina_amqp import task

from guillotina_notification.utility_ws import INotificationSender
#from guillotina_notification.utility_email import post_notification_in_email_queue
#from guillotina_notification.statics_vars import STATUS_NOT_NOTIFIED

from guillotina.component import query_utility
from guillotina.interfaces import IMailer

from guillotina.request import record

import json
import uuid

'''
decido per ora di passare 3 parametri:
receverId------>lo userId che userò per cercare la socket
                fra quelle aperte e per poterle tracciare dopo, vedremo poi se sia possibile o meno

message-------->la notifica che dovrò inviare, la gestisco come Text

subject-------->Il titolo utile alle email

app------------>il nome della applicazione che uso come Folder per salvare le notifiche di ogni utente

status--------->non inviato, ma usato, uso 2 stati fissi
                NOT_NOTIFIED
                NOTIFIED
'''

@task
async def post_new_notification_wsocket(receverId, message, app):

    #import pdb; pdb.set_trace()
    parent =  get_current_container()

    #parent = await parent.async_get(app)
    subject = ("Notification for/to " + receverId)

    random_id = ('Notify_to_' + receverId + '_' + str(len(message)) + '_' + str(len(receverId)) + '_' + str(len(app)))

    notification = await create_content_in_container(
                parent, 'Notification', 
                random_id, id=random_id,
                check_security=False,
                receverId=receverId, message=message, 
                subject=subject,
                status='NOT_NOTIFIED', application_name=app)

    print('Scritto nel db')

    #utility = get_utility(INotificationSender)
    #await utility.post_notification_in_ws_queue(notification)

'''
ok cosa gli passo qui come destinatario...email o receverId?
'''
@task
async def post_new_notification_email(email_recipient, subject, message, app):

    #import pdb; pdb.set_trace()
    parent =  get_current_container()

    #parent = await parent.async_get(app)
    random_id = ('Notify_to_' + email_recipient + '_' + str(len(subject)))

    notification = await create_content_in_container(
                parent, 'Notification', 
                random_id, id=random_id,
                check_security=False,
                receverId=email_recipient, message=message, 
                subject=subject,
                status='NOT_NOTIFIED', application_name=app)


    print('Scritto nel db')

    mailer = query_utility(IMailer)
    #idealmente send(recipient=email, subject=subject, text=message)
    await mailer.send(recipient=email_recipient, subject=subject, text=message)
