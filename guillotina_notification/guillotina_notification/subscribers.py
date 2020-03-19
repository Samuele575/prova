from guillotina import configure

from guillotina.component import get_utility
from guillotina.interfaces import IObjectAddedEvent

from guillotina.utils import get_current_request

from guillotina_notification.content import INotification
from guillotina_notification.utility_ws import INotificationSender

from guillotina.component import query_utility
from guillotina.interfaces import IMailer

@configure.subscriber(for_=(INotification, IObjectAddedEvent))
async def notification_added(notification, event):
    
    print('Sono dentro il subscriber e mi attivo quando aggiungo una nuova notifica')

    if notification.not_type == 'SIMPLE': 
        utility = get_utility(INotificationSender)
        await utility.post_notification_in_ws_queue(notification)
    elif notification.not_type == 'EMAIL':
        mailer = query_utility(IMailer)
        #idealmente send(recipient=email, subject=subject, text=message)
        await mailer.send(recipient=email, subject=subject, text=message)

