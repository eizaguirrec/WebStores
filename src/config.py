import os

DEBUG = True
ADMINS = frozenset([
    os.environ.get('ADMINS')
])

print(ADMINS)

