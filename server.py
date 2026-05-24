#!/usr/bin/env python3
"""Server for Mentor AI — injects .env vars into the frontend.

Usage:
    python server.py [port]
"""
import os,sys,re,json
from http.server import HTTPServer,SimpleHTTPRequestHandler
from pathlib import Path

DIR = Path(__file__).parent
ENV_FILE = DIR / '.env'

def load_env():
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k,v = line.split('=',1)
                env[k.strip()] = v.strip()
    return env

ENV = load_env()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):
        super().__init__(*a,directory=str(DIR),**kw)

    def do_GET(self):
        if self.path == '/__env':
            self.send_response(200)
            self.send_header('Content-Type','application/json')
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()
            self.wfile.write(json.dumps(ENV).encode())
            return
        super().do_GET()

    def send_head(self):
        path = self.translate_path(self.path)
        if path == DIR / 'index.html':
            # read original, inject env
            html = path.read_text(encoding='utf-8')
            script = '<script>window.__ENV__='+json.dumps(ENV)+'</script>'
            html = html.replace('</head>',script+'</head>')
            # serve modified
            self.send_response(200)
            self.send_header('Content-Type','text/html; charset=utf-8')
            self.send_header('Content-Length',str(len(html.encode())))
            self.send_header('Last-Modified',self.date_time_string())
            self.end_headers()
            return html.encode()
        return super().send_head()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv)>1 else 9876
    srv = HTTPServer(('0.0.0.0',port),Handler)
    provider = ENV.get('PROVIDER','?')
    print(f'Mentor AI running at http://localhost:{port}')
    print(f'  Provider: {provider}  |  Key: {"set" if ENV.get("API_KEY") else "missing"}')
    print(f'  Edit .env to change settings.  Ctrl+C to stop.')
    try: srv.serve_forever()
    except KeyboardInterrupt: print('\nStopped.')
