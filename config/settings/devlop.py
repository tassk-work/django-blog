from .base import *

ALLOWED_HOSTS = ['*']

MIDDLEWARE.insert(0, 'config.log.LogMiddleware')

CONTENTS_DIR = os.path.join(BASE_DIR.parent, 'django-blog-contents')

DATABASES['default']['NAME'] = os.path.join(CONTENTS_DIR, 'db.sqlite3')

TEMPLATES[0]['DIRS'] = [os.path.join(CONTENTS_DIR, 'templates')]

DEBUG = True

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(CONTENTS_DIR, 'static'),
]

# codestart:LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(process)d %(thread)d %(clientIp)-15s %(levelname)-5s %(name)s.%(funcName)s %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)-5s %(name)s.%(funcName)s %(message)s'
        },
        'operation': {
            'format': '%(asctime)s %(clientIp)-15s %(requestPath)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'operation': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'operation',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'blog': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'blog.operation': {
            'handlers': ['operation'],
            'level': 'INFO',
        },
    }
}
from .. import log
# codeend:LOGGING

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True

try:
    from .local import *
except ImportError:
    pass
