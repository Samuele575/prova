from guillotina import testing
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager

import json
import pytest


def base_settings_configurator(settings):
    if 'applications' in settings:
        settings['applications'].append('guillotina_notification')
    else:
        settings['applications'] = ['guillotina_notification']


testing.configure_with(base_settings_configurator)


class guillotina_notification_Requester(ContainerRequesterAsyncContextManager):  # noqa

    async def __aenter__(self):
        await super().__aenter__()
        resp = await self.requester(
            'POST', '/db/guillotina/@addons',
            data=json.dumps({
                'id': 'guillotina_notification'
            })
        )
        return self.requester


@pytest.fixture(scope='function')
async def guillotina_notification_requester(guillotina):
    return guillotina_notification_Requester(guillotina)
