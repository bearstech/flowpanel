from aiohttp.web import Application

from .auth import auth_factory
from .controler import home, websocket_handler, event


app = Application(middlewares=[auth_factory])
app.router.add_route('GET', '/', home)
app.router.add_route('GET', '/chaussette', websocket_handler)
app.router.add_route('PUT', '/event/{user}', event)
