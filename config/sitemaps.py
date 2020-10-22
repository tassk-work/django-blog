from django.db.models import Max
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog import models

# codestart:AuthorSitemap
class AuthorSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return models.Author.objects.values('id','user__username').annotate(updated_date=Max('blog__updated_date')).order_by('id')

    def location(self, obj):
        return reverse('blog:index', args=[obj['user__username']])

    def lastmod(self, obj):
        return obj['updated_date']
# codeend:AuthorSitemap

# codestart:BlogSitemap
class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 1.0

    def items(self):
        return models.Blog.objects.filter(status=models.BlogStatus.PUBLIC)

    def location(self, obj):
        return reverse('blog:detail', args=[obj.author.user.username, obj.id])

    def lastmod(self, obj):
        return obj.updated_date
# codeend:BlogSitemap

sitemaps = {
    'author': AuthorSitemap,
    'blog': BlogSitemap,
}