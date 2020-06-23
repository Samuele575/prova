from guillotina import configure, content, Interface, schema


class INotification(Interface):

    #the type of the notification: EMAIL or SIMPLE
    not_type = schema.TextLine(
        title="Notification type"
    )

    recipientId = schema.Text(
        title="Recipient identifier"
    )
    email_recipient = schema.TextLine(
        title="Recipient email"
    )

    #title
    subject = schema.Text(
        title="Notification title"
    )
    message = schema.Text(
        title="Body of the notification"
    )

    #the name of the application that call the send.py
    application_name = schema.Text(
        title="The FrontEnd name"
    )
    
    #When it's triggered the event 
    notification_date = schema.TextLine(
        title="Notification Date"
    )
    
    #the status of the notification: NOTIFIED or NOT_NOTIFIED
    status = schema.Text(
        title="Notification status"
    )


@configure.contenttype(
    type_name="Notification",
    schema=INotification,
    behaviors=[
        "guillotina.behaviors.dublincore.IDublinCore",
        "guillotina.behaviors.attachment.IAttachment"])
class Notification(content.Item):
    pass
