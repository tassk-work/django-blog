import re
import logging
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.views import generic

from blog import forms
from blog import models
from blog.lib import constants

from . import base

# codestart:BlogList
class BlogList(generic.ListView):
    model = models.Blog
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.kwargs['author'].id)
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status__gte=models.BlogStatus.PUBLIC)
        return queryset.order_by('-view_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object_list = context['object_list']
        for blog in object_list:
            blog.categories = list(blog.blogcategories_set.all())
        return context
# codeend:BlogList

# codestart:BlogIndex
class BlogIndex(base.CommonMixin, BlogList):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logging.getLogger(constants.OPERATION_LOG).info('')
        return context
# codeend:BlogIndex

# codestart:BlogSearch
class BlogSearch(base.CommonMixin, BlogList):
    template_name = 'blog/search.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.form = None

    def get_query(self, keyword):
        category_ids = []
        search_words = []
        category_keywords = re.findall(r'category:[^ 　]+', keyword)
        if category_keywords:
            for category_keyword in category_keywords:
                category_text = re.findall(r'category:([^ 　]+)', category_keyword)[0]
                category = models.Category.objects.get(author=self.kwargs['author'].id,category_text=category_text)
                if category:
                    category_ids.append(category.id)
                    keyword = keyword.replace(category_keyword, '').strip()
        
        if keyword:
            search_words = re.split(r'[ 　]+', keyword)

        queries = [Q(author=self.kwargs['author'].id)]
        category_ids = list(set(category_ids))
        if category_ids:
            queries.append(Q(blogcategories__category_id__in=category_ids))

        search_words = list(set(search_words))
        if search_words:
            text_query = Q(search_text__contains=search_words.pop())
            for search_word in search_words:
                text_query &= Q(search_text__contains=search_word)
            queries.append(text_query)

        search_query = queries.pop()
        for query in queries:
            search_query &= query
        return search_query

    def get_queryset(self):
        self.form = forms.SearchForm(self.request.GET or None)
        queryset = super().get_queryset()
        if self.form.is_valid():
            keyword = self.form.cleaned_data['keyword'].strip()
            if (keyword):
                queryset = queryset.filter(self.get_query(keyword))
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        log_contents = {}
        if self.form.is_valid():
            log_contents['keyword'] = self.form.cleaned_data['keyword'].strip()
        logging.getLogger(constants.OPERATION_LOG).info(log_contents)
        return context
# codeend:BlogSearch