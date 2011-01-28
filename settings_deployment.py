from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

import os

f = open(os.getenv('HOME')+'/passwords/db-focus.txt', 'rb')
DB_PASSWORD = f.readline().strip()
f.close()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'frecarlsen_focus',
        'USER':'frecarlsen',
        'PASSWORD':DB_PASSWORD,
    }
}
