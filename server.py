import asyncio

from flowpanel.app import init


loop = asyncio.get_event_loop()

srv, handler, app = loop.run_until_complete(init(loop))
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
