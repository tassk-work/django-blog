import logging
import random
import re
from django import template
from django.db.models import Count
from django.utils import html

from blog import models
from blog.lib import utils

logger = logging.getLogger(__name__)

# codestart:category_summary
register = template.Library()

@register.inclusion_tag('blog/category_summary.html', takes_context=True)
def category_summary(context, author_id):
    posts = models.Post.objects.filter(
                author=author_id,
                status__gte=models.PostStatus.PUBLIC,
                postcontent__language_code=context.request.LANGUAGE_CODE,
            )
    return {
        "categories": models.PostCategory.objects.values('category__id', 'category__category_text')
            .filter(post__in=posts).annotate(Count('post')),
    }
# codeend:category_summary

# codestart:post_favor
@register.inclusion_tag('blog/post_favor.html', takes_context=True)
def post_favor(context, author_id, count):
    return {
        "favor_posts": models.PostContent.objects.filter(
                post__author=author_id,
                language_code=context.request.LANGUAGE_CODE,
                post__status__gte=models.PostStatus.PUBLIC
            ).order_by('-post__view_count')[:count]
    }
# codeend:post_favor

@register.filter
def striptags2(tag_str):
    tag_str = html.strip_tags(tag_str)
    tag_str = re.sub(r'\s+', ' ', tag_str)
    return tag_str

@register.filter
def strip(str):
    return str.strip();

@register.simple_tag(takes_context=True)
def get_ads_index(context, length):
    ads_data = context.request.session.get('ads_data')
    if ads_data:
        i = ads_data['index'] + 1
        if i >= len(ads_data['list']):
            i = 0
        ads_data['index'] = i
    else:
        l = list(range(length))
        random.shuffle(l)
        logger.info(f'ads list:{l}')
        ads_data = { 'list':l, 'index':0}
    
    context.request.session['ads_data'] = ads_data
    return ads_data['list'][ads_data['index']]
