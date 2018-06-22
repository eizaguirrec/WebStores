import os

DEBUG = True
PORT = '4990'
HOST = ''
ADMINS = frozenset([
    os.environ.get('ADMINS')
])

