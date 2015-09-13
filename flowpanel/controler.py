import asyncio
import json
from pathlib import Path

import asyncio_redis
from aiohttp import web, MsgType
from aiohttp.websocket import Message
from asyncio_redis.replies import PubSubReply

from .auth import USER_KEY

MIMES_EXTENSION = {
    'html': 'text/html',
    'js': 'application/javascript',
    'css': 'text/css',
}


@asyncio.coroutine
def static(request):
    path = Path("static/%s" % request.match_info.get('file', 'index.html'))
    if not path.exists():
        raise web.HTTPNotFound()
    return web.Response(body=path.open('rb').read(),
                        content_type=MIMES_EXTENSION.get(path.suffix[1:]))


@asyncio.coroutine
def event(request):
    user = request.match_info['user']
    if not request.has_body:
        raise web.HTTPBadRequest
    connection = request.app['redis']
    body = yield from request.content.read()
    yield from connection.publish('/events/%s' % user,
                                  str(body, encoding='utf-8'))

    return web.Response(status=201)


@asyncio.coroutine
def websocket_handler(request):
    global USER_KEY

    if USER_KEY not in request:
        raise web.HTTPForbidden
    print("User", request[USER_KEY])
    ws = web.WebSocketResponse()
    ws.start(request)

    ws.send_str("START")
    connection = request.app['redis']
    pong = yield from connection.ping()
    assert pong.status == "PONG"

    subscriber = yield from connection.start_subscribe()
    chan = yield from subscriber.subscribe(['/events/%s' % request[USER_KEY], '/events'])
    todos = set([ws.receive(), subscriber.next_published()])
    while True:
        done, todos = yield from asyncio.wait(todos, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            result = task.result()
            if type(result) == Message:
                msg = result
                if msg.tp == MsgType.text:
                    if msg.data == 'close':
                        yield from ws.close()
                        yield from connection.close()
                    else:
                        print('ws message', msg.data)
                        ws.send_str(msg.data + '/answer')
                elif msg.tp == MsgType.close:
                    print('websocket connection closed')
                    yield from connection.close()
                elif msg.tp == MsgType.error:
                    print('ws connection closed with exception %s',
                        ws.exception())
                todos.add(ws.receive())
            elif type(result) == PubSubReply:
                reply = result
                print(reply)
                ws.send_str(json.dumps(dict(chan=reply.channel,
                                            value=reply.value)))
                todos.add(subscriber.next_published())
            else:
                print("type unknown", type(result))
    return ws

