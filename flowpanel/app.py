import asyncio
from aiohttp.web import Application
import asyncio_redis

from .auth import auth_factory
from .controler import static, websocket_handler, event

@asyncio.coroutine
def close_redis(self):
    self['redis'].close()


@asyncio.coroutine
def init(loop):
    app = Application(middlewares=[auth_factory])
    app['redis'] = yield from asyncio_redis.Pool.create(host='127.0.0.1',
                                                        port=6379, poolsize=10)
    app.register_on_finish(close_redis)

    app.router.add_route('GET', '/', static)
    app.router.add_route('GET', '/static/{file}', static)
    app.router.add_route('GET', '/chaussette', websocket_handler)
    app.router.add_route('PUT', '/event/{user}', event)
    handler = app.make_handler()
    srv = yield from loop.create_server(handler, '0.0.0.0', 8080)
    return srv, handler, app
