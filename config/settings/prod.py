from config.settings.base import *

#Override base.py

DEBUG = False

ALLOWED_HOSTS = ['boardingapp.herokuapp.com', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd4jn462hqt36up',
        'HOST': 'ec2-176-34-116-203.eu-west-1.compute.amazonaws.com',
        'PORT' : 5432,
        'USER' : 'nfuuzgzuukbelk',
        'PASSWORD' : '0a55ff836b23a0256e78bebb478a2c59b293d3ef54a9b263f6510645fe83bd9e'
    }
}