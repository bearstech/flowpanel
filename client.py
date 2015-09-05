import asyncio

import aiohttp


@asyncio.coroutine
def client():
    ws = yield from aiohttp.ws_connect(
        'http://beuha:@localhost:8080/chaussette')

    while True:
        msg = yield from ws.receive()

        if msg.tp == aiohttp.MsgType.text:
            if msg.data == 'close':
                yield from ws.close()
                break
            else:
                print(msg.data)
                #ws.send_str(msg.data + '/answer')
        elif msg.tp == aiohttp.MsgType.closed:
            break
        elif msg.tp == aiohttp.MsgType.error:
            break

loop = asyncio.get_event_loop()
loop.run_until_complete(client())
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
loop.close()
