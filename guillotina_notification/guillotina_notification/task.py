from guillotina import task_vars as g_task_vars

from guillotina.component import get_utility #getUtilty
from guillotina.content import create_content_in_container
from guillotina.utils import get_current_request, get_current_container
from guillotina.interfaces import IRolePermissionManager, IObjectAddedEvent

from guillotina.event import notify
from guillotina.events import  ObjectAddedEvent

from guillotina_amqp import task

from guillotina_notification.content import INotification
from guillotina_notification.utility_ws import INotificationSender

from guillotina.component import query_utility
from guillotina.interfaces import IMailer

import json
import uuid
import random

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
async def post_new_notification(not_type, recipientId, email, message, app):

    #import pdb; pdb.set_trace()
    parent =  get_current_container()

    #parent = await parent.async_get(app)
    subject = ("Notification for/to " + recipientId)

    random_id = ('Notify_to_' + recipientId + '_' + str(len(message)+random.randint(0,10)) + '_' + str(len(recipientId)+random.randint(0,10)) + '_' + str(len(app)+random.randint(0,10)))

    notification = await create_content_in_container(
                parent, 'Notification', 
                random_id, id=random_id,
                check_security=False, not_type=not_type,
                recipientId=recipientId, message=message, 
                email_recipient=email, subject=subject,
                status='NOT_NOTIFIED', application_name=app,
                creators=('root',), contributors=('root',))
    roleperm = IRolePermissionManager(notification)
    roleperm.grant_permission_to_role(
        'guillotina.AddContent', 'guillotina.Member')
    roleperm.grant_permission_to_role(
        'guillotina.AccessContent', 'guillotina.Member')
    

    print('Scritto nel db')

    utility = get_utility(INotificationSender)
    utility.set_Navigator()

    await notify(ObjectAddedEvent(notification, parent, random_id))

'''
ok cosa gli passo qui come destinatario...email o receverId?
@task
async def post_new_notification_email(not_type, recipientId, email, subject, message, app):

    #import pdb; pdb.set_trace()
    parent =  get_current_container()

    #parent = await parent.async_get(app)
    random_id = ('Notify_to_' + email + '_' + str(len(subject)))

    notification = await create_content_in_container(
                parent, 'Notification', 
                random_id, id=random_id,
                check_security=False, not_type=not_type,
                recipientId=recipientId, email_recipient=email, message=message, 
                subject=subject, status='NOT_NOTIFIED', application_name=app)

    print('Scritto nel db')

    mailer = query_utility(IMailer)
    #idealmente send(recipient=email, subject=subject, text=message)
    await mailer.send(recipient=email, subject=subject, text=message)
    '''