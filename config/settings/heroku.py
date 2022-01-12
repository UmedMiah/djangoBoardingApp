"""
Production Settings for Heroku
"""

import environ

from config.settings.base import * # noqa

env = environ.Env(
    DEBUG=(bool, False)
)

# False if not in os.environ
DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

DATABASES = {
    'default': env.db(),
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 1200
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

X_FRAME_OPTIONS = 'DENY'

SECURE_BROWSER_XSS_FILTER = True
