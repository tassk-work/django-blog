from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.db.models import Max
from django.urls import reverse

from blog import models
from blog.lib import common

# codestart:BlogSitemap
class BlogSitemap(Sitemap):

    def reverse(self, obj):
        pass

    def location(self, obj):
        path = self.reverse(obj)
        if obj['language_code'] == settings.LANGUAGE_CODE:
            return path
        else:
            return f'/{obj["language_code"]}{path}'

    def get_urls(self, page=1, site=None, protocol=None):
        urls = super().get_urls(page, site, protocol)

        # alternate
        kwalternates_w = {}
        for url in urls:
            obj = url['item']
            alternates = kwalternates_w.get(obj['key'], [])
            kwalternates_w[obj['key']] = alternates
            alternates.append({
                'lang_code': obj['language_code'],
                'location': url['location'],
            })
        # alternate x-default
        kwalternates = {}
        for key, alternates in kwalternates_w.items():
            if len(alternates) < 2:
                continue
            alternate_default = next((a for a in alternates if a['lang_code'] == 'en'), None)
            if not alternate_default:
                alternate_default = next((a for a in alternates if a['lang_code'] == settings.LANGUAGE_CODE), None)
            alternates.append({
                'lang_code': 'x-default',
                'location': alternate_default['location'],
            })
            kwalternates[key] = alternates

        for url in urls:
            obj = url['item']
            alternates = kwalternates.get(obj['key'])
            if alternates:
                url['alternates'] = alternates
        return urls
# codeend:BlogSitemap

# codestart:AuthorSitemap
class AuthorSitemap(BlogSitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        items = models.PostContent.objects.values_list('post__author__user__username', 'language_code') \
                .annotate(updated_date=Max('post__updated_date')).order_by('post__author_id')
        return [{'key':item[0], 'language_code':item[1], 'updated_date':item[2]} for item in items]

    def reverse(self, obj):
        return reverse('blog:index', args=(obj['key'],))

    def lastmod(self, obj):
        return obj['updated_date']
# codeend:AuthorSitemap

# codestart:PostSitemap
class PostSitemap(BlogSitemap):
    changefreq = "never"
    priority = 1.0

    def items(self):
        items = models.PostContent.objects.values_list('post__id', 'post__author__user__username', 'language_code') \
                .annotate(updated_date=Max('post__updated_date')).order_by('post__author_id')
        return [{
                'key': f'{item[0]},{item[1]}',
                'id': item[0],
                'auth_name': item[1],
                'language_code': item[2],
                'updated_date': item[3],
            } for item in items]

    def reverse(self, obj):
        return reverse('blog:detail', args=(obj['auth_name'], obj['id'],))

    def lastmod(self, obj):
        return obj['updated_date']
# codeend:PostSitemap

sitemaps = {
    'author': AuthorSitemap,
    'post': PostSitemap,
}