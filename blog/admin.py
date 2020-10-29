from django.contrib import admin
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.utils.html import format_html

from . import models
from blog.lib import utils

# codestart:AuthorUser
class AuthorInline(admin.StackedInline):
    model = models.Author
    max_num = 1
    can_delete = False

class AuthorUser(AuthUserAdmin):
    inlines = [AuthorInline]

admin.site.unregister(AuthUser)
admin.site.register(AuthUser, AuthorUser)
# codeend:AuthorUser

# codestart:AplModel
def set_author_by_user(request, org_list, item_name):
    edit_list = list(org_list)
    if not request.user.is_superuser:
        edit_list.remove(item_name)
    return edit_list    

class AplModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(author=request.user.author)
        return queryset

    def get_list_display(self, request):
        return set_author_by_user(request, super().get_list_display(request), 'author')

    def get_list_filter(self, request):
        return set_author_by_user(request, super().get_list_filter(request), 'author')
    
    def get_exclude(self, request, obj=None):
        exclude = super().get_exclude(request, obj)
        if not request.user.is_superuser:
            if not exclude:
                exclude = []
            exclude.append('author')
        return exclude
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.author = request.user.author
        obj.save()
# codeend:AplModel

# codestart:RelatedModel
class RelatedModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            queryset = queryset.filter(post__author=request.user.author)
        return queryset
    
    def author(sef, obj):
        return obj.post.author
    
    def get_list_display(self, request):
        return set_author_by_user(request, super().get_list_display(request), 'author')
    
    def get_list_filter(self, request):
        return set_author_by_user(request, super().get_list_filter(request), 'post__author')
# codeend:RelatedModel

# codestart:Author
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'title_text_link', 'email', 'flags', 'post')
    ordering = ('id',)
    search_fields = ('author_name', 'title_text', 'email')
    exclude = ('user',)

    def author_name(sef, obj):
        return obj.user.username

    def title_text_link(sef, obj):
        href = reverse('blog:index', kwargs={'author_name':obj.user.username})
        return format_html('<a href="{}" target="blog">{}</a>', href, obj.title_text)
    title_text_link.short_description = 'title_text'

    def post(sef, obj):
        href = reverse('blog:index', kwargs={'author_name':obj.user.username})
        return format_html('<a href="{}" target="blog">{}</a>', href, obj.post_set.count())

    def email(sef, obj):
        return obj.user.email

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(models.Author, AuthorAdmin)
# codeend:Author

# codestart:Post
class PostAdmin(AplModelAdmin):
    list_display = ['id', 'author', 'title_text', 'status', 'template_text', 'category', 'view_count']
    ordering = ('author', 'id')
    list_filter = ['author', 'status']
    search_fields = ('template_text',)
    
    def title_text(sef, obj):
        href = reverse('blog:detail', kwargs={'author_name':obj.author.user.username, 'pk':obj.id})
        return format_html('<a href="{}" target="blog">{}</a>', href, obj.get_title_text())

    def category(sef, obj):
        return obj.postcategory_set.count()

admin.site.register(models.Post, PostAdmin)
# codeend:Post

# codestart:PostContent
class PostContentAdmin(RelatedModelAdmin):
    list_display = ('id', 'post', 'language_code_short', 'title_text_link', 'summary_text_short')
    ordering = ('post', 'id', 'language_code')
    list_filter = ('post__author', 'language_code')
    search_fields = ('language_code', 'title_text', 'summary_text')
    raw_id_fields = ('post',)

    def language_code_short(sef, obj):
        return obj.language_code
    language_code_short.short_description = 'lang'

    def title_text_link(sef, obj):
        href = utils.reverse('blog:detail', obj.language_code, {
            'author_name': obj.post.author.user.username,
            'pk': obj.post.id
        })
        return format_html('<a href="{}" target="blog">{}</a>', href, obj.title_text)
    title_text_link.short_description = "title_text"

    def summary_text_short(sef, obj):
        return obj.summary_text[:20]
    summary_text_short.short_description = "summary_text"

admin.site.register(models.PostContent, PostContentAdmin)
# codeend:PostContent


# codestart:Category
class CategoryAdmin(AplModelAdmin):
    list_display = ('author', 'category_text', 'order_number')
    ordering = ('author', 'order_number')
    list_filter = ('author',)
    search_fields = ('category_text',)
    
admin.site.register(models.Category, CategoryAdmin)
# codeend:Category

# codestart:PostCategory
class PostCategoryAdmin(RelatedModelAdmin):
    list_display = ('author', 'category', 'post')
    ordering = ('category', 'post')
    list_filter = ('post__author', 'category')
    search_fields = ('category', 'post')
    raw_id_fields = ('category', 'post')
    
admin.site.register(models.PostCategory, PostCategoryAdmin)
# codeend:PostCategory

# codestart:Comment
class CommentAdmin(RelatedModelAdmin):
    list_display = ('author', 'id', 'comment_text', 'status', 'client_text', 'post', 'parent', 'created_date')
    ordering = ('-id',)
    list_filter = ('post__author', 'status',)
    search_fields = ('comment_text', 'post', 'client_text')

admin.site.register(models.Comment, CommentAdmin)
# codeend:Comment