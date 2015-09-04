import asyncio
import base64

from aiohttp.web import HTTPUnauthorized


USER_KEY = 'basic_auth_user'


@asyncio.coroutine
def auth_factory(app, handler):
    @asyncio.coroutine
    def middleware(request):
        print(request.headers)
        if 'AUTHORIZATION' not in request.headers:
            return web.Response(
                headers={'WWW-Authenticate': 'Basic realm="flowpanel"'},
                status=HTTPUnauthorized.status_code)
        else:
            auth, loginpassword = request.headers['AUTHORIZATION'].split(" ", 2)
            assert auth == "Basic"
            login, password = base64.b64decode(loginpassword).decode('utf-8').split(':', 2)
            # FIXME, validate the password
            request[USER_KEY] = login

        return (yield from handler(request))
    return middleware
