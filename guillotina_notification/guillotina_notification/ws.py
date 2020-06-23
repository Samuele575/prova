import asyncio
import logging

import aiohttp
from aiohttp import web
from guillotina import configure
from guillotina.component import get_utility
from guillotina.interfaces import IContainer
from guillotina.transactions import get_tm

from guillotina.utils import get_current_request  

from guillotina_notification.utility_ws import INotificationSender

logger = logging.getLogger('guillotina_notification')

@configure.service(
    context=IContainer, method='GET', allow_access=True,
    permission='guillotina.AccessContent', name='@notificate')
async def ws_notificate(context, request):
    ws = web.WebSocketResponse()
    utility = get_utility(INotificationSender)
    utility.register_ws(ws)

    tm = get_tm()
    await tm.abort()
    await ws.prepare(request)

    try:
        async for msg in ws:
            if msg.tp == aiohttp.WSMsgType.text:
                #la nostra socket non riceve nessun messaggio, li invia solo
                pass
            elif msg.tp == aiohttp.WSMsgType.error:
                logger.debug(
                    'ws connection closed with exception {0:s}'.format(ws.exception()))
    except (RuntimeError, asyncio.CancelledError):
        pass
    finally:
        logger.debug('websocket connection closed')
        utility.unregister_ws(ws)

    return {}
