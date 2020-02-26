from guillotina import configure

from guillotina.component import get_utility
from guillotina.interfaces import IObjectAddedEvent

from guillotina.utils import get_current_request


from guillotina_notification.content import INotification
from guillotina_notification.utility_ws import INotificationSender


@configure.subscriber(for_=(INotification, IObjectAddedEvent))
async def notification_added(notification, event):
    
    print('Sono dentro il subscriber e mi attivo quando aggiungo una nuova notifica')

    #utility = get_utility(INotificationSender)
    #await utility.send_message(notification)


