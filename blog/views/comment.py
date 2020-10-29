import logging
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from ipware import get_client_ip

from blog import forms
from blog import mails
from blog import models
from blog.lib import constants
from blog.lib import common

logger = logging.getLogger(__name__)

# codestart:comment
def comment(request, *args, **kwargs):
    post = get_object_or_404(models.Post, pk=kwargs['post_id'])
    if not post.is_comment or not post.is_comment_entry:
        raise PermissionDenied

    form = forms.CommentForm(request.POST or None)
    if not form.is_valid():
        return JsonResponse({
            'status': 11,
            'message': _('Input Error'),
        })
    
    comment = form.save(commit=False)
    comment.post = post
    comment.client_text = get_client_ip(request)[0]
    comment.save()

    mails.comment_notification(request, comment)
    logging.getLogger(constants.OPERATION_LOG).info({'post':post.id})
    return JsonResponse({
        'status': 1,
        'message': _('COMMENT_REGISTERED'),
    })
# codeend:comment

# codestart:reply
def reply(request, *args, **kwargs):
    parent = get_object_or_404(models.Comment, pk=kwargs['comment_id'])

    if not common.has_perm(request, constants.PERMISSION_COMMENT_REPLY, post=parent, author=kwargs['author']):
        raise PermissionDenied

    form = forms.CommentForm(request.POST or None)
    if not form.is_valid():
        return JsonResponse({
            'status': 11,
            'message': _('Input Error'),
        })
    
    comment = form.save(commit=False)
    comment.post = parent.post
    comment.parent = parent
    comment.client_text = get_client_ip(request)[0]
    comment.save()

    logging.getLogger(constants.OPERATION_LOG).info({'post':parent.post.id, 'parent':parent.id})
    return JsonResponse({
        'status': 1,
        'message': _('REPLY_REGISTERED'),
    })
# codeend:reply

# codestart:comment_update
def comment_update(request, *args, **kwargs):
    comment = get_object_or_404(models.Comment, pk=kwargs['comment_id'])
    if not common.has_perm(request, constants.PERMISSION_COMMENT_EDIT, post=comment.post, author=kwargs['author']):
        raise PermissionDenied
    form = forms.CommentForm(request.POST or None)
    status = form['status'].data
    if not status:
        return JsonResponse({
            'status': 11,
            'message': _('Input Error'),
        })
    comment.status = int(status)
    comment.save()
    
    logging.getLogger(constants.OPERATION_LOG).info({'post':comment.post.id, 'comment':comment.id})
    return JsonResponse({
        'status': 1,
        'data': {
            'status': comment.status,
            'status_name': str(models.CommentStatus(comment.status))
        },
        'message': _('COMMENT_UPDATED'),
    })
# codeend:comment_update