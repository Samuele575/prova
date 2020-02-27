from guillotina import configure, content, Interface, schema

class INotification(Interface):

    not_type = schema.TextLine()
    recipientId = schema.Text()
    email_recipient = schema.TextLine()
    subject = schema.Text()
    message = schema.Text()
    application_name = schema.Text()
    status = schema.Text()


@configure.contenttype(
    type_name="Notification",
    schema=INotification,
    behaviors=[
        "guillotina.behaviors.dublincore.IDublinCore",
        "guillotina.behaviors.attachment.IAttachment"])
class Notification(content.Item):
    pass
