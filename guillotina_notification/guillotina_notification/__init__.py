from guillotina import configure


app_settings = {
    "load_utilities": {
        "guillotina_notification.notification_sender": {
            "provides": "guillotina_notification.utility_ws.INotificationSender",
            "factory": "guillotina_notification.utility_ws.NotificationSenderUtility",
            "settings": {}
        },
    }
}
    

def includeme(root):
    """
    custom application initialization here
    """

    configure.scan('guillotina_notification.content') #1 creo la classe: Notification
    configure.scan('guillotina_notification.serialize') #2 implemento la serializzazione delle notifiche
    configure.scan('guillotina_notification.utility_ws') #3 L'UTILITI che gestisce le socket con le applicazioni 
    configure.scan('guillotina_notification.services') #4 le 2 chiamate get-notification NOTIFIED e NOT_NOTIFIED
    
    configure.scan('guillotina_notification.task') #5 le nuove services.py, che implementano i metodi per la creazione di notifiche
    configure.scan('guillotina_notification.subscribers') #6 test per vedere se una semplice create_content_in_container triggera un evento

    configure.scan('guillotina_notification.behaviors') #provo a creare la lista di socket aperte attraverso dei behaviors
    configure.scan('guillotina_notification.ws') #gestione apertura di una web_socket

    configure.scan('guillotina_notification.api')
    configure.scan('guillotina_notification.install')
