from guillotina.async_util import IAsyncUtility
from guillotina.component import getMultiAdapter
from guillotina.interfaces import IResourceSerializeToJsonSummary
from guillotina.renderers import GuillotinaJSONEncoder
from guillotina.utils import get_current_request, Navigator, find_container, get_current_container

from guillotina.transactions import get_tm, get_transaction

import aiohttp
from aiohttp import web

import asyncio
import json
import logging

logger = logging.getLogger('guillotina_notification')


class INotificationSender(IAsyncUtility):
    pass


class NotificationSenderUtility:

    def __init__(self, settings=None, loop=None, navigator=None):
        self._loop = loop
        self._settings = {}
        self._webservices = []
        self.navigator = navigator

    def register_ws(self, ws):
        request = get_current_request()

        multi_params = request.query_string

        for parametro in multi_params.split('&'):
            ricercato = parametro.split('=')
            if ricercato[0] == 'userId':
                ws.user_id = ricercato[1]

        self._webservices.append(ws)

        print(ws.user_id)

        '''
        context.webservices.append(ws)
        context.register()
        print(ws.user_id)
        '''

    def unregister_ws(self, ws):
        self._webservices.remove(ws)


    async def post_notification_in_ws_queue(self, notification):
        summary = await getMultiAdapter(
            (notification, get_current_request()),
            IResourceSerializeToJsonSummary)()

        await self._queue.put((notification, summary))


    async def initialize(self, app=None):
        self._queue = asyncio.Queue()

        while True:
            try:
                notification, summary = await self._queue.get()
                
                #test
                print("Appena tirato fuori la notifica dalla coda")
                for ws in self._webservices:
                    #test per sapere se esistono le ws
                    print(ws.user_id)
                    if notification.recipientId == ws.user_id:
                        #test per capire se la ricerca va a buon fine
                        print(notification.status)
                        await ws.send_str(json.dumps(
                            summary, cls=GuillotinaJSONEncoder))
                
            except Exception:
                logger.warn(
                    'Error sending notification',
                    exc_info=True)
                await asyncio.sleep(1)
