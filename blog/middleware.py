from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from . import models
from .lib import constants

class BaseMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    # codestart:process_view
    def process_view(self, request, view_func, view_args, view_kwargs):
        author_name = view_kwargs.get('author_name')
        if author_name:
            author = models.Author.objects.get(user__username=author_name)
            if author:
                view_kwargs['author'] = author
                posts = models.Post.objects.values('id', 'template_text').filter(author=author.id)
                view_kwargs['post_ids']  = {post['template_text']:post['id'] for post in posts}
        session_messages = request.session.pop(constants.SESSION_MESSAGES, None)
        if session_messages:
            for message in session_messages:
                if message['level'] == messages.INFO:
                    messages.info(request, message['message'])
                elif message['level'] == messages.WARNING:
                    messages.warning(request, message['message'])
                elif message['level'] == messages.ERROR:
                    messages.error(request, message['message'])
        return None
    # codeend:process_view