import os
import re
from django.db.models import Max
from django.core.management.base import BaseCommand
from blog import models

URL_ELEMENT_AUTHOR = '<url><loc>https://tassk.work/blog/{0}/</loc><lastmod>{1}</lastmod></url>'
URL_ELEMENT_BLOG = '<url><loc>https://tassk.work/blog/{0}/{1}</loc><lastmod>{2}</lastmod></url>'

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, *args, **options):
        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        
        authors = models.Author.objects.values('id','name_text').annotate(updated_date=Max('blog__updated_date'))
        for author in authors:
            if author['updated_date']:
                url = URL_ELEMENT_AUTHOR.format(author['name_text'], author['updated_date'].strftime('%Y-%m-%dT%H:%M:%SZ'))
                lines.append(url)        

        blogs = models.Blog.objects.filter(status=models.BlogStatus.PUBLIC)
        for blog in blogs:
            url = URL_ELEMENT_BLOG.format(blog.author.user.username, blog.id, blog.updated_date.strftime('%Y-%m-%dT%H:%M:%SZ'))
            lines.append(url)
        lines.append('</urlset>')

        with open(options['path'], 'w') as f:
            f.write("\n".join(lines))
