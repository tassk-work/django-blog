import logging
import random
import re
from django import template
from django.db.models import Count
from django.utils import html

from blog import models

logger = logging.getLogger(__name__)

# codestart:category_summary
register = template.Library()

@register.inclusion_tag('blog/category_summary.html')
def category_summary(author_id):
    return {
        "categories": models.BlogCategories.objects.values('category__id', 'category__category_text')
            .filter(category__author=author_id).annotate(Count('blog')),
    }
# codeend:category_summary

# codestart:blog_favor
@register.inclusion_tag('blog/blog_favor.html')
def blog_favor(author_id, count):
    return {
        "favor_blogs": models.Blog.objects
            .filter(author=author_id, status__gte=models.BlogStatus.PUBLIC)
            .order_by('-view_count')[:count]
    }
# codeend:blog_favor

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
