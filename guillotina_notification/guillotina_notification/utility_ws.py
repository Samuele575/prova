from guillotina.async_util import IAsyncUtility
from guillotina.component import getMultiAdapter
from guillotina.interfaces import IResourceSerializeToJsonSummary
from guillotina.renderers import GuillotinaJSONEncoder
from guillotina.utils import get_current_request

from guillotina.transactions import get_tm, get_transaction

import aiohttp
from aiohttp import web

import time
import asyncio
import json
import logging

logger = logging.getLogger('guillotina_notification')


class INotificationSender(IAsyncUtility):
    pass


class NotificationSenderUtility:

    def __init__(self, settings=None, loop=None):
        self._loop = loop
        self._settings = {}
        self._webservices = []

    def register_ws(self, ws):
        request = get_current_request()

        multi_params = request.query_string

        for parametro in multi_params.split('&'):
            ricercato = parametro.split('=')
            if ricercato[0] == 'userId':
                ws.user_id = ricercato[1]
            elif ricercato[0] == 'appliction':
                ws.app_name = ricercato[1]

        self._webservices.append(ws)

    def unregister_ws(self, ws):
        self._webservices.remove(ws)


    async def post_notification_in_ws_queue(self, notification, s):
        summary = await getMultiAdapter(
            (notification, get_current_request()),
            IResourceSerializeToJsonSummary)()

        await self._queue.put((notification, summary, s))


    async def initialize(self, app=None):
        self._queue = asyncio.Queue()

        while True:
            try:
                notification, summary, s = await self._queue.get()
                
                for ws in self._webservices:

                    if notification.recipientId == ws.user_id and notification.application_name == ws.app_name:
                        await ws.send_str(json.dumps(
                            summary, cls=GuillotinaJSONEncoder))

                        elapsed = time.perf_counter() - s
                        print(f"{__file__} executed in {elapsed:0.2f} seconds.")
                    #else: 
                    #    elapsed = time.perf_counter() - s
                    #    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
                
            except Exception:
                logger.warn(
                    'Error sending notification',
                    exc_info=True)
                await asyncio.sleep(1)
