from guillotina import configure
from guillotina.component import getMultiAdapter
from guillotina.interfaces import IContainer, IResourceSerializeToJsonSummary

from guillotina.utils import get_current_container #, get_current_request

#notification of only the "NOT_NOTIFIED" notification
@configure.service(for_=IContainer, name='@get-new-notifications',
                   permission='guillotina.Authenticated')
async def get_new_notification(context, request):
    results = []

    container =  get_current_container()
    
    '''
    from the request we need 3 param:  
    
    ::param: userId
    ::param: application_name
    ::param: notification_type
    '''

    multi_params = request.query_string

    user_Id = 0
    application_name = ''
    notification_type = 'SIMPLE'

    for parametro in multi_params.split('&'):
        ricercato = parametro.split('=')
        if ricercato[0] == 'notification_type':
            if ricercato[1] == 'EMAIL':
                notification_type = 'EMAIL'
            else: 
                notification_type = 'SIMPLE'

        elif  ricercato[0] == 'application_name':
            application_name = ricercato[1]

        elif  ricercato[0] == 'userId' or ricercato[0] == 'email': 
            user_Id = ricercato[1]

    #only the notific. with status = NOT_NOTIFIED
    async for item in context.async_values():
        #if 'Notification' == getattr(item, "type_name"): 
        if getattr(item, "not_type") == notification_type and getattr(item, "application_name") == application_name and getattr(item, "recipientId") == user_Id and getattr(item, "status") == "NOT_NOTIFIED":
            summary = await getMultiAdapter(
                (item, request),
                IResourceSerializeToJsonSummary)()
            results.append(summary)
    
    #sort the results list
    results = sorted(results, key=lambda conv: conv['notification_date'])
    return results



#all the notification related to user_id and application_name
@configure.service(for_=IContainer, name='@get-notifications',
                   permission='guillotina.Authenticated')
async def get_all_notifications(context, request):
    results = []

    container =  get_current_container()

    multi_params = request.query_string

    user_Id = "foobar"
    application_name = "Django"
    notification_type = "SIMPLE"

    
    for parametro in multi_params.split('&'):
        ricercato = parametro.split('=')
        if ricercato[0] == 'notification_type':
            if ricercato[1] == 'EMAIL':
                notification_type = 'EMAIL'
            else: 
                notification_type = 'SIMPLE'

        elif  ricercato[0] == 'application_name':
            application_name = ricercato[1]

        elif  ricercato[0] == 'userId' or ricercato[0] == 'email': 
            user_Id = ricercato[1]

        print(ricercato[1])
    
    #all the notific. related to a userId/email
    async for item in context.async_values():
        if 'Notification' == getattr(item, "type_name"):
            if getattr(item, "not_type") == notification_type and getattr(item, "application_name") == application_name and getattr(item, "recipientId") == user_Id:
                summary = await getMultiAdapter(
                    (item, request),
                    IResourceSerializeToJsonSummary)()
                results.append(summary)
    
    #usato per ordinare i risultati in uscita
    results = sorted(results, key=lambda conv: conv['notification_date'])
    return results