from guillotina import configure, content, Interface, schema


class INotification(Interface):

    #the type of the notification: EMAIL or SIMPLE
    not_type = schema.TextLine()

    recipientId = schema.Text()
    email_recipient = schema.TextLine()

    #title
    subject = schema.Text()
    message = schema.Text()

    #the name of the application that call the send.py
    application_name = schema.Text()

    #the status of the notification: NOTIFIED or NOT_NOTIFIED
    status = schema.Text()


@configure.contenttype(
    type_name="Notification",
    schema=INotification,
    behaviors=[
        "guillotina.behaviors.dublincore.IDublinCore",
        "guillotina.behaviors.attachment.IAttachment"])
class Notification(content.Item):
    pass
