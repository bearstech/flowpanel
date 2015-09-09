Flow panel
==========

Display live events in a webpage.

It uses Python 3.4, asyncio, redis and websockets.

Try it
------

Install the dependencies with python 3.4.

    virtualenv -p python3.4 .
    ./bin/pip install -r requirements.txt

Launch redis server

Run the server

    ./bin/python server.py

The panel is here : http://localhost:8080/

You can use the CLI client

    ./bin/python client.py

You can send events with HTTP

    curl -v -XPUT -d 'uhuhu' http://beuha:@localhost:8080/event/beuha

Or directly with Redis

    redis-cli
    PUBLISH /events "broadcast event"

Status
------

Explosive alpha.

Licence
-------

3 terms BSD Licence, © 2015 Mathieu Lecarme
