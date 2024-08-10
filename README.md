I wanted to look into how one could turn a phone into something like an xbox controller. I have learned a lot and made this in the process. I might turn it into my original thought in the future. Have fun! :)

Create a Virtual Environment and activate it.
```bash
python -m venv venv
venv\Scripts\activate
```

Install the requirements and start the servers.
```bash
pip install -r requirements.txt
python main.py
```

This file will start 2 servers:
1. HTTP server that only serves the index.html file http://x.x.x.x:1000. (Port also might be different),
2. Websoket server, the actual code that does the mouse control. ws://x.x.x.x:2000 (Port also might be different)

The terminal will give the links. Visit the http server on your phone then enter ws server address fully. Something like 'ws://x.x.x.x:2000'.