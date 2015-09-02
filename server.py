import asyncio
import asyncio_redis
from aiohttp import web, MsgType

@asyncio.coroutine
def home(request):
    return web.Response(body=open('index.html', 'rb').read(), content_type="text/html")


@asyncio.coroutine
def websocket_handler(request):

    ws = web.WebSocketResponse()
    ws.start(request)

    ws.send_str("START")
    connection = yield from asyncio_redis.Connection.create(host='127.0.0.1', port=6379)
    pong = yield from connection.ping()
    print(pong)

    while True:
        msg = yield from ws.receive()

        if msg.tp == MsgType.text:
            if msg.data == 'close':
                yield from ws.close()
                yield from connection.close()
            else:
                ws.send_str(msg.data + '/answer')
        elif msg.tp == MsgType.close:
            print('websocket connection closed')
            yield from connection.close()
        elif msg.tp == MsgType.error:
            print('ws connection closed with exception %s',
                  ws.exception())

    return ws


app = web.Application()
app.router.add_route('GET', '/', home)
app.router.add_route('GET', '/chaussette', websocket_handler)

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
