import json
from django.conf import settings
from django.template import loader
from django.urls import reverse as django_reverse

def tostr(dict):
    return json.dumps(dict)

def get_template(template_name):
    try:
        return loader.get_template(template_name)
    except:
        pass

def get_template_lang(request):
    return '' if request.LANGUAGE_CODE == settings.LANGUAGE_CODE else f'{request.LANGUAGE_CODE}/'

def get_template_path(request, parent, template_name):
    parent_path = f'{parent}/' if parent else ''
    template_string = f'blog/{parent_path}{{0}}{template_name}.html'
    template_path = template_string.format(get_template_lang(request))
    template = get_template(template_path)
    return template_path if template else template_string.format('')

def get_languages(request, available_languages):
    enable_languages = []
    selectable_languages = []
    for language in settings.LANGUAGES:
        if language[0] in available_languages:
            enable_languages.append(language)
            if language[0] != request.LANGUAGE_CODE:
                selectable_languages.append(language)
    if selectable_languages:
        return selectable_languages if len(selectable_languages) == 1 else enable_languages

def reverse(viewname, language_code, *args):
    lang = '' if language_code == settings.LANGUAGE_CODE else f'/{language_code}'
    return f'{lang}{django_reverse(viewname, args=args)}'
