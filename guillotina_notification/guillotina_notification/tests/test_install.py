import asyncio


async def test_install(guillotina_notification_requester):  # noqa
    async with guillotina_notification_requester as requester:
        response, _ = await requester('GET', '/db/guillotina/@addons')
        assert 'guillotina_notification' in response['installed']
