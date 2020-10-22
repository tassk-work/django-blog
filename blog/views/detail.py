import logging
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.views import generic
from . import base
from blog import forms
from blog import models
from blog.lib import constants
from blog.lib import common
from blog.lib import utils

logger = logging.getLogger(__name__)

# codestart:BlogDetail
class BlogDetail(base.CommonMixin, generic.DetailView):
    model = models.Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.kwargs['author'].id)
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status__gte=models.BlogStatus.PUBLIC)
        return queryset

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_authenticated:
            obj.view_count += 1
            obj.save()
        obj.categories = list(obj.blogcategories_set.all())
        comment_status = models.CommentStatus.UNAPPROVED if self.request.user.is_authenticated else models.CommentStatus.APPROVED
        if obj.is_comment:
            comments = list(obj.comment_set.filter(status__gte=comment_status))
            parents = []
            replydict = dict() 
            for comment in comments:
                comment.status_name = str(models.CommentStatus(comment.status))
                if comment.parent:
                    replies = replydict.get(comment.parent.id, [])
                    replies.append(comment)
                    replydict[comment.parent.id] = replies
                else:
                    parents.append(comment)
            for comment in parents:
                comment.replies = replydict.get(comment.id)
            obj.comments = parents
            obj.is_comment_edit = common.has_perm(self.request, constants.PERMISSION_COMMENT_EDIT, blog=obj, author=self.kwargs['author'])
            obj.is_comment_reply = common.has_perm(self.request, constants.PERMISSION_COMMENT_REPLY, blog=obj, author=self.kwargs['author'])
        self.template_name = f'blog/{self.kwargs["author_name"]}/{obj.template_text}.html'

        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = forms.CommentForm(None)
        logging.getLogger(constants.OPERATION_LOG).info({'blog':self.object.id})
        return context
# codeend:BlogDetail

class BlogDetailTest(generic.DetailView):
    model = models.Blog
    template_name = 'blog/detail_test.html'

    def get_object(self):
        obj = models.Blog()
        obj.id = 0
        obj.title_text = f'test {self.kwargs["author_name"]}/{self.kwargs["template_name"]}'
        obj.template_text = self.kwargs['template_name']
        obj.created_date = timezone.now()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_template'] = f'blog/{self.kwargs["author_name"]}/{self.object.template_text}.html'
        return context
