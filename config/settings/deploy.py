from .base import *

ALLOWED_HOSTS = ['*']

MIDDLEWARE.insert(0, 'config.log.LogMiddleware')

CONTENTS_DIR = os.path.join(BASE_DIR.parent, 'djang-blog-contents')

DATABASES['default']['NAME'] = os.path.join(CONTENTS_DIR, 'db.sqlite3')

TEMPLATES[0]['DIRS'] = [os.path.join(CONTENTS_DIR, 'templates')]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(CONTENTS_DIR, 'static'),
]

DEFAULT_AUTHOR = 'sysja'

DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(thread)d %(clientIp)-15s %(levelname)-5s %(name)s.%(funcName)s %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)-5s %(name)s.%(funcName)s %(message)s'
        },
        'operation': {
            'format': '%(asctime)s %(clientIp)-15s %(requestPath)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/django.log'),
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'operation': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'log/operation.log'),
            'maxBytes': 1024 * 1024 * 1,
            'backupCount': 5,
            'formatter': 'operation',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'blog': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'blog.operation': {
            'handlers': ['operation'],
            'level': 'INFO',
        },
    }
}
from .. import log

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
