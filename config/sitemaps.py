from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.db.models import Max
from django.urls import reverse

from blog import models
from blog.lib import common

# codestart:BlogSitemap
class BlogSitemap(Sitemap):
    def get_language_codes(self, url):
        pass

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page, site, protocol)
        for url in urls:
            language_codes = self.get_language_codes(url)
            if len(language_codes) < 2:
                continue
            alternates = []
            default_location = url['location']
            for language_code in language_codes:
                if settings.LANGUAGE_CODE == language_code:
                    location = url['location']
                else:
                    location = f'{protocol}://{site}/{language_code}{self.location(url["item"])}'
                alternates.append({
                    'lang_code': language_code,
                    'location': location,
                })
                if language_code == 'en':
                    default_location = location
            
            alternates.append({
                'lang_code': 'x-default',
                'location': default_location,
            })
            url['alternates'] = alternates
        return urls
# codeend:BlogSitemap

# codestart:AuthorSitemap
class AuthorSitemap(BlogSitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return models.Author.objects.values('id','user__username').annotate(updated_date=Max('post__updated_date')).order_by('id')

    def location(self, obj):
        return reverse('blog:index', args=[obj['user__username']])

    def lastmod(self, obj):
        return obj['updated_date']
    
    def get_language_codes(self, url):
        return common.get_author_language_codes(url['item']['id'])
# codeend:AuthorSitemap

# codestart:PostSitemap
class PostSitemap(BlogSitemap):
    changefreq = "never"
    priority = 1.0

    def items(self):
        return models.Post.objects.filter(status=models.PostStatus.PUBLIC).order_by('id')

    def location(self, obj):
        return reverse('blog:detail', args=[obj.author.user.username, obj.id])

    def lastmod(self, obj):
        return obj.updated_date
    
    def get_language_codes(self, url):
        return common.get_post_language_codes(url['item'].id)
# codeend:PostSitemap

sitemaps = {
    'author': AuthorSitemap,
    'post': PostSitemap,
}