import logging
import threading
from ipware import get_client_ip

# codestart:001
old_factory = logging.getLogRecordFactory()

threadinglocal = threading.local()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    clientIp, requestPath = '', ''
    if hasattr(threadinglocal, 'request'):
        clientIp = get_client_ip(threadinglocal.request)[0]
        requestPath = threadinglocal.request.path
    record.clientIp = clientIp
    record.requestPath = requestPath
    return record

logging.setLogRecordFactory(record_factory)

class LogMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        threadinglocal.request = request
        return self.get_response(request)
# codeend:001


