import os
import re
import datetime
from django.core.management.base import BaseCommand
from blog import models

# codestart:001
WORD_EXCLUDES = ('public', 'void', 'null', 'var', 'return')
RE_PATTERNS = (
    (r'{% templatetag openblock %}', ''),
    (r'{% templatetag closeblock %}', ''),
    (r'{% templatetag openvariable %}', ''),
    (r'{% templatetag closevariable %}', ''),
    (r'{% templatetag opencomment %}', ''),
    (r'{% templatetag closecomment %}', ''),
    (r'{% templatetag openbrace %}', ''),
    (r'{% templatetag closebrace %}', ''),
    (r'<.+?>',''),
    (r'&lt;.+?&gt;',''),
    (r'[;!=?,]+', ' '),
)
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('templates')

    def handle(self, *args, **options):
        blog_list = models.Blog.objects.all()
        for blog in blog_list:
            path = f'{options["templates"]}/blog/{blog.author.user.username}/{blog.template_text}.html'
            contents = self.read(path)
            blog.title_text = contents['blog_title']
            blog.summary_text = self.edit_summary(contents['blog_content'])
            content_search = self.edit_search(contents['blog_content'])
            blog.search_text = f'{blog.title_text} {content_search}'
            blog.updated_date = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            blog.save()
            print(f'{blog.id}:{blog.title_text},{blog.summary_text[:20]},{blog.search_text[:20]},{blog.updated_date}')
    
    def read(self, path):
        with open(path,'r') as f:
            text = f.read()
        return {
            'blog_title': re.search(r'{% block blog_title %}\s*(.*?)\s*{% endblock %}', text).group(1),
            'blog_content': re.search(r'{% block blog_content %}(.*){% endblock %}', text, re.DOTALL).group(1),
        }
    
    def edit_summary(self, content):
        summary = re.search(r'<p.*?>\s*(.*?)\s*</p>', content, flags=re.DOTALL).group(1)
        for re_pattern in RE_PATTERNS:
            summary = re.sub(re_pattern[0], re_pattern[1], summary)
        summary = re.sub(r'\s+', ' ', summary)
        return summary

    def edit_search(self, html):
        html_text = html
        for re_pattern in RE_PATTERNS:
            html_text = re.sub(re_pattern[0], re_pattern[1], html_text)
        html_words = set(re.split(r'\s+',  html_text))
        words = []
        for word in html_words:
            if (len(word) < 2):
                continue
            if word in WORD_EXCLUDES:
                continue
            words.append(word)
        search_text = ' '.join(words)
        return search_text
# codeend:001