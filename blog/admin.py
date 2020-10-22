from django.contrib import admin
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.urls import reverse
from django.utils.html import format_html

from . import models

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
            queryset = queryset.filter(blog__author=request.user.author)
        return queryset
    
    def author(sef, obj):
        return obj.blog.author
    
    def get_list_display(self, request):
        return set_author_by_user(request, super().get_list_display(request), 'author')
    
    def get_list_filter(self, request):
        return set_author_by_user(request, super().get_list_filter(request), 'blog__author')
# codeend:RelatedModel

# codestart:Author
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'title_text', 'email', 'template_text', 'flags', 'blog')
    ordering = ('id',)
    search_fields = ('author_name', 'title_text', 'email', 'template_text')
    exclude = ('user',)

    def author_name(sef, obj):
        return obj.user.username

    def blog(sef, obj):
        href = reverse('blog:index', kwargs={'author_name':obj.user.username})
        return format_html('<a href="{}" target="blog">{}</a>', href, obj.blog_set.count())

    def email(sef, obj):
        return obj.user.email

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(models.Author, AuthorAdmin)
# codeend:Author

# codestart:Blog
class BlogAdmin(AplModelAdmin):
    list_display = ['author', 'id', 'title_text_link', 'status', 'template_text_link', 'category', 'view_count']
    ordering = ('author', 'id')
    list_filter = ['author', 'status']
    search_fields = ('title_text', 'template_text')
    
    def title_text_link(sef, obj):
        href = reverse('blog:detail', kwargs={'author_name':obj.author.user.username, 'pk':obj.id})
        return format_html('<a href="{}" target="blog">{}</a>', href, obj.title_text)
    title_text_link.short_description = "title_text"

    def template_text_link(sef, obj):
        href = reverse('blog:detail_test', kwargs={'author_name':obj.author.user.username, 'template_name':obj.template_text})
        return format_html('<a href="{}" target="blog">{}</a>', href, obj.template_text)
    template_text_link.short_description = "template_text"

    def category(sef, obj):
        return obj.blogcategories_set.count()

admin.site.register(models.Blog, BlogAdmin)
# codeend:Blog

# codestart:Category
class CategoryAdmin(AplModelAdmin):
    list_display = ('author', 'category_text', 'order_number')
    ordering = ('author', 'order_number')
    list_filter = ('author',)
    search_fields = ('category_text',)
    
admin.site.register(models.Category, CategoryAdmin)
# codeend:Category

# codestart:BlogCategories
class BlogCategoriesAdmin(RelatedModelAdmin):
    list_display = ('author', 'category', 'blog')
    ordering = ('category', 'blog')
    list_filter = ('blog__author', 'category')
    search_fields = ('category', 'blog')
    raw_id_fields = ('category', 'blog')
    
admin.site.register(models.BlogCategories, BlogCategoriesAdmin)
# codeend:BlogCategories

# codestart:Comment
class CommentAdmin(RelatedModelAdmin):
    list_display = ('author', 'id', 'comment_text', 'status', 'client_text', 'blog', 'parent', 'created_date')
    ordering = ('-id',)
    list_filter = ('blog__author', 'status',)
    search_fields = ('comment_text', 'blog', 'client_text')

admin.site.register(models.Comment, CommentAdmin)
# codeend:Comment