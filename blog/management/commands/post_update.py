import os
import re
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from blog import models

# codestart:Const
WORD_EXCLUDES = ('public', 'void', 'null', 'var', 'return')
RE_PATTERNS = (
    (r'^.*# code(start|end).*$', ''),
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
# codeend:Const

# codestart:Command
class Command(BaseCommand):

    def get_template_path(self, author_name, language_code, template_text):
        lang_path = '' if language_code == settings.LANGUAGE_CODE else f'{language_code}/'
        template_relpath = f'/blog/{author_name}/{lang_path}{template_text}.html'
        for dir in settings.TEMPLATES[0]['DIRS']:
            template_path = f'{dir}/{template_relpath}'
            if os.path.exists(template_path):
                return template_path

    def handle(self, *args, **options):
        posts = models.Post.objects.all()
        for post in posts:
            timestamps = []
            for language_code in [l[0] for l in settings.LANGUAGES]:
                template_path = self.get_template_path(post.author.user.username, language_code, post.template_text)
                if not template_path:
                    continue
                contents = self.read(template_path)
                post_content = post.postcontent_set.get(language_code=language_code)
                if post_content:
                    process = 'UPDATE'
                else:
                    post_content =  models.PostContent()
                    post_content.post = post
                    post_content.language_code = language_code
                    process = 'INSERT'
                post_content.title_text = contents['title']
                post_content.summary_text = self.edit_summary(contents['content'])
                content_search = self.edit_search(contents['content'])
                post_content.search_text = f'{post_content.title_text} {content_search}'
                post_content.save()
                print(f'  Content:{process}:{post_content.id},{post_content.language_code},{post_content.title_text},{post_content.summary_text[:20]},{post_content.search_text[:20]}')
                timestamps.append(os.path.getmtime(template_path))
        
            post.updated_date = timezone.make_aware(datetime.datetime.fromtimestamp(max(timestamps)))
            post.save()
            print(f'Post:{post.id},{len(timestamps)},{post.updated_date}')
    
    def read(self, path):
        with open(path,'r') as f:
            text = f.read()
        return {
            'title': re.search(r'{% block post_title %}\s*(.*?)\s*{% endblock %}', text).group(1),
            'content': re.search(r'{% block post_content %}(.*){% endblock %}', text, re.DOTALL).group(1),
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
# codeend:Command