from aiohttp.web import Application

from .auth import auth_factory
from .controler import static, websocket_handler, event


app = Application(middlewares=[auth_factory])
app.router.add_route('GET', '/', static)
app.router.add_route('GET', '/static/{file}', static)
app.router.add_route('GET', '/chaussette', websocket_handler)
app.router.add_route('PUT', '/event/{user}', event)
