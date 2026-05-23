#!/usr/bin/env python3
"""Unified Server for Mentor AI.
Serves both the landing page (index.html at root) and the chat app (character-ai/index.html).
Injects environment variables from character-ai/.env into the chat app.
"""
import os
import sys
import json
import io
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

DIR = Path(__file__).parent.resolve()
CHAR_AI_DIR = DIR / 'character-ai'
ENV_FILE = CHAR_AI_DIR / '.env'

def load_env():
    env = {}
    if ENV_FILE.exists():
        try:
            for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
        except Exception as e:
            print(f"Error loading .env: {e}")
    return env

ENV = load_env()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(DIR), **kw)

    def do_GET(self):
        # Serve the environment configuration
        if self.path in ('/__env', '/api/env', '/character-ai/__env'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(ENV).encode('utf-8'))
            return
            
        # Route root-level characters.json to character-ai/characters.json
        if self.path == '/characters.json':
            self.path = '/character-ai/characters.json'

        super().do_GET()

    def send_head(self):
        path = Path(self.translate_path(self.path))
        # If serving character-ai/index.html, inject the environment variables
        if path.is_file() and path.resolve() == (CHAR_AI_DIR / 'index.html').resolve():
            try:
                html = path.read_text(encoding='utf-8')
                script = '<script>window.__ENV__=' + json.dumps(ENV) + '</script>'
                html = html.replace('</head>', script + '</head>')
                
                html_bytes = html.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(html_bytes)))
                self.send_header('Last-Modified', self.date_time_string())
                self.end_headers()
                return io.BytesIO(html_bytes)
            except Exception as e:
                print(f"Error serving index.html: {e}")
                
        return super().send_head()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    srv = HTTPServer(('0.0.0.0', port), Handler)
    provider = ENV.get('PROVIDER', '?')
    print(f'Mentor AI Server running at http://localhost:{port}')
    print(f'  Landing Page: http://localhost:{port}/')
    print(f'  Chat App:     http://localhost:{port}/character-ai/')
    print(f'  Provider: {provider}  |  Key: {"set" if ENV.get("API_KEY") else "missing"}')
    print(f'  Press Ctrl+C to stop.')
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\nStopped.')
