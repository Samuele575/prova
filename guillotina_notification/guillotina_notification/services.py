from guillotina import configure
from guillotina.component import getMultiAdapter
from guillotina.interfaces import IContainer, IResourceSerializeToJsonSummary

from guillotina.utils import get_current_container #, get_current_request


#--------------------------------------
@configure.service(for_=IContainer, name='@get-notifications-notified',
                   permission='guillotina.Authenticated')
async def get_notification_view(context, request):
    results = []

    container =  get_current_container()

    '''
    request = get_current_request()
    '''
    
    #idealmente è un singolo parametro
    multi_params = request.query_string

    user_Id = 0
    #quindi il 'for' è idealmente inutile
    for parametro in multi_params.split('&'):
        ricercato = parametro.split('=')
        if ricercato[0] == 'userId': 
            user_Id = ricercato[1]


    async for item in container.async_values():
        '''
        allora perche lo chiamo 'item' e non 'notification'?
        perchè l'uso della utility per le email FORZA 
        l'installazione di guillotina_dbusers
        quindi NON TUTTI GLI ELEMENTI IN QUESTO CONTAINER SONO NOTIFICHE
        avrò anche 2 Folder: 'users' e 'groups'
        '''
        if 'Notification' == getattr(item, "type_name"): 
            #qui idealmente si può mettere anche la ricerca sull'email
            if getattr(item, "receverId") == user_Id and getattr(item, "status") == "NOTIFY":
                summary = await getMultiAdapter(
                    (item, request),
                    IResourceSerializeToJsonSummary)()
                results.append(summary)
    
    #usato per ordinare i risultati in uscita
    results = sorted(results, key=lambda conv: conv['creation_date'])
    return results


#--------------------------------------
@configure.service(for_=IContainer, name='@get-notifications-not-notified',
                   permission='guillotina.Authenticated')
async def get_conversations(context, request):
    results = []

    container =  get_current_container()

    '''
    request = get_current_request()
    '''
    
    #idealmente è un singolo parametro
    multi_params = request.query_string

    user_Id = 0
    #quindi il 'for' è inutile
    for parametro in multi_params.split('&'):
        ricercato = parametro.split('=')
        if  ricercato[0] == 'userId': 
            user_Id = ricercato[1]


    async for item in container.async_values():
        if 'Notification' == getattr(item, "type_name"): 
            #qui idealmente si può mettere anche la ricerca sull'email
            if getattr(item, "receverId") == user_Id and getattr(item, "status") == "NOT_NOTIFY":
                summary = await getMultiAdapter(
                    (item, request),
                    IResourceSerializeToJsonSummary)()
                results.append(summary)
    
    #usato per ordinare i risultati in uscita
    results = sorted(results, key=lambda conv: conv['creation_date'])
    return results



#------------------------------------------------------
    '''
    idealmente quando vado a prendere le notifiche
    di un solo utente, legato all'user_ID
    quindi potrei anche fare collassare le 2 @get-notification
    '''
@configure.service(for_=IContainer, name='@get-notifications',
                   permission='guillotina.Authenticated')
async def get_notification(context, request):
    results = []

    container =  get_current_container()

    '''
    request = get_current_request()
    '''
    
    multi_params = request.query_string

    print(multi_params)

    user_Id = 0

    for parametro in multi_params.split('&'):
        ricercato = parametro.split('=')
        if ricercato[0] == 'userId': 
            user_Id = ricercato[1]


    async for item in container.async_values():
        if 'Notification' == getattr(item, "type_name"): 
            #qui idealmente si può mettere anche la ricerca sull'email
            if getattr(item, "receverId") == user_Id:
                summary = await getMultiAdapter(
                    (item, request),
                    IResourceSerializeToJsonSummary)()
                results.append(summary)
    
    #usato per ordinare i risultati in uscita
    results = sorted(results, key=lambda conv: conv['creation_date'])
    return results