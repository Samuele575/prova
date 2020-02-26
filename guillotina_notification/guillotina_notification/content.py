from guillotina import configure
from guillotina import schema
from guillotina import interfaces
from guillotina import content

class INotification(interfaces.IItem):

    receverId = schema.Text()
    subject = schema.Text()
    message = schema.Text()
    application_name = schema.Text()
    status = schema.Text()

    #secondo me si potrebbe mettere anche l'email come schema
    #del tipo: 
    #email_recipient: schema.TextLine() una linea senza \n o \r


@configure.contenttype(
    type_name="Notification",
    schema=INotification)
class Notification(content.Item):
    pass
