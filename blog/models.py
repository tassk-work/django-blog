import logging
import datetime
from django.conf import settings as django_settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as _lazy
from .lib import constants

logger = logging.getLogger(__name__)

# codestart:Author
class Author(models.Model):
    user = models.OneToOneField(django_settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title_text = models.CharField(max_length=100)
    aside_text = models.TextField(max_length=1000)
    template_text = models.CharField(max_length=20, null=True, blank=True)
    flags = models.IntegerField(default=0, help_text=_lazy('AUTHOR_FLAGS_HELP'))
    
    def __str__(self):
        return f'{self.user.username}:{self.title_text}'

    @property
    def is_comment(self):
        return self.flags & constants.AuthorFlag.COMMENT_FLAG.value > 0
# codeend:Author

# codestart:AplModel
class AplModel(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True
# codeend:AplModel        

# codestart:Blog
class BlogStatus(models.IntegerChoices):
    DRAFT = 1
    PRIVATE = 2
    PUBLIC = 3
    DELETED = -1

class Blog(AplModel):
    title_text = models.CharField(max_length=100, null=False, blank=True, help_text=_lazy('BLOG_TITLE_HELP'))
    summary_text = models.CharField(max_length=1000, null=True, blank=True, help_text=_lazy('BLOG_TITLE_HELP'))
    status = models.IntegerField(choices=BlogStatus.choices, default=BlogStatus.DRAFT)
    search_text = models.CharField(max_length=5000, null=False, blank=True, help_text=_lazy('BLOG_TITLE_HELP'))
    template_text = models.CharField(max_length=20)
    flags = models.IntegerField(default=0, help_text=_lazy('BLOG_FLAGS_HELP'))
    view_count = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(null=False, blank=True, default=timezone.now, help_text=_lazy('BLOG_TITLE_HELP'))

    def __str__(self):
        return f'{self.title_text}:{str(self.status)}'

    @property
    def is_comment(self):
        return self.author.is_comment and self.flags & constants.BlogFlag.COMMENT_FLAG.value > 0
    
    def get_comment_count(self, gt_date):
        return Comment.objects.filter(blog=self.id,created_date__gt=gt_date).count()
    
    def get_comment_day_count(self):
        return self.get_comment_count(timezone.now()-datetime.timedelta(days=1));
    
    @property
    def is_comment_entry(self):
        count = self.get_comment_day_count()
        return count <= 10
# codeend:Blog

# codestart:Category
class Category(AplModel):
    category_text = models.CharField(max_length=20)
    order_number = models.IntegerField()

    def __str__(self):
        return self.category_text
# codeend:Category

# codestart:BlogCategories
class BlogCategories(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category}:{self.blog}'
# codeend:BlogCategories

# codestart:Comment
class CommentStatus(models.IntegerChoices):
    UNAPPROVED = 1, 'Unapproved'
    APPROVED = 2, 'Approved'
    DELETED = -1, 'Deleted'

    def get_choices():
        return [(c.value, _(c.label)) for c in CommentStatus]

    def __str__(self):
        return _(self.label)

class Comment(models.Model):
    name_text = models.CharField(max_length=100, null=False, blank=True)
    comment_text = models.TextField(max_length=1000)
    status = models.IntegerField(choices=CommentStatus.choices, default=CommentStatus.UNAPPROVED)
    client_text = models.CharField(max_length=20)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.status:
            self.status = CommentStatus.UNAPPROVED
        self.created_date = timezone.now()
        super().save(args, kwargs)

    def __str__(self):
        return f'{str(self.blog.id)}:{self.comment_text[:10]}'
# codeend:Comment