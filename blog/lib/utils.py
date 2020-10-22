import json

def get_language(request):
    # request.LANGUAGE_CODE
    return request.LANGUAGE_CODE if request.LANGUAGE_CODE == 'ja' else 'en'

def tostr(dict):
    return json.dumps(dict)