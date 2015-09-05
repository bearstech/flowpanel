import asyncio
from base64 import b64decode

from aiohttp.web import HTTPUnauthorized


USER_KEY = 'basic_auth_user'


@asyncio.coroutine
def auth_factory(app, handler):
    @asyncio.coroutine
    def middleware(request):
        if 'AUTHORIZATION' not in request.headers:
            raise HTTPUnauthorized(
                    headers={'WWW-Authenticate': 'Basic realm="flowpanel"'}
            )
        else:
            auth, loginpassword = request.headers['AUTHORIZATION'].split(" ", 2)
            assert auth == "Basic"
            login, password = b64decode(loginpassword).decode('utf-8').split(':', 2)
            # FIXME, validate the password
            request[USER_KEY] = login

        return (yield from handler(request))
    return middleware
