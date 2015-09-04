import asyncio
from aiohttp.web import Application


from flowpanel.auth import auth_factory
from flowpanel.controler import home, websocket_handler, event



app = Application(middlewares=[auth_factory])
app.router.add_route('GET', '/', home)
app.router.add_route('GET', '/chaussette', websocket_handler)
app.router.add_route('PUT', '/event/{user}', event)

loop = asyncio.get_event_loop()
handler = app.make_handler()
f = loop.create_server(handler, '0.0.0.0', 8080)
srv = loop.run_until_complete(f)
print('serving on', srv.sockets[0].getsockname())
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(handler.finish_connections(1.0))
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.run_until_complete(app.finish())
loop.close()
