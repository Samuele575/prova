from guillotina import configure
from guillotina.interfaces import IResourceSerializeToJsonSummary
from guillotina.json.serialize_content import DefaultJSONSummarySerializer
from guillotina.utils import get_owners
from guillotina_notification.content import INotification
from zope.interface import Interface


@configure.adapter(
    for_=(INotification, Interface),
    provides=IResourceSerializeToJsonSummary)
class NotificationJSONSummarySerializer(DefaultJSONSummarySerializer):
    async def __call__(self):
        data = await super().__call__()
        data.update({
            #per ora passo l'ID della notifica
            'id': self.context.id,
            'creation_date': self.context.creation_date,
	    
            #serializzo le notifiche
            'receverId': self.context.receverId,
            'subject': self.context.subject,
            'message': self.context.message,
            'application_name': self.context.application_name,
            'status': self.context.status,
             
            #se volessimo essere precisi: 'author': Django-Freeman 
	        'author': get_owners(self.context)[0] #sempre root idealmente
        })
        return data
