import logging
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from blog import models
from blog.lib import constants
from blog.lib import common
from blog.lib import utils

logger = logging.getLogger(__name__)

# codestart:redirect_view
def redirect_view(request):
    url = request.GET.get('url')
    if url:
        message = request.GET.get('message')
        if message:
            request.session[constants.SESSION_MESSAGES] = [
                {'level': int(request.GET.get('message_level', messages.INFO)),'message' :_(message)}
            ]
        return redirect(url)
    else:
        logger.error('Parameter Error')
        raise Http404
# codeend:redirect_view

# codestart:default_view
def default_view(request):
    if hasattr(settings, 'DEFAULT_AUTHOR') and settings.DEFAULT_AUTHOR:
        return redirect('blog:index', settings.DEFAULT_AUTHOR)
    else:
        logger.error('settings.DEFAULT_AUTHOR is not defined.')
        raise Http404
# codeend:default_view

# class CommonMixin(generic.base.TemplateResponseMixin):
# codestart:CommonMixin
class CommonMixin():
    def get_template_names(self):
        template = super().get_template_names()
        self.kwargs['base_template'] = template[0]
        language_codes = common.get_author_language_codes(self.kwargs['author'].id)
        self.kwargs['available_languages'] = utils.get_languages(self.request, language_codes)
        template[0] = utils.get_template_path(self.request, self.kwargs['author_name'], 'extends')
        logger.debug(f'{self.kwargs["base_template"]}:{template[0]}')
        return template
# codeend:CommonMixin
