from . import constants
from blog import models

def has_perm(request, permission, **kwargs):
    if permission == constants.PERMISSION_COMMENT_EDIT:
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user == kwargs['author'].user
        )
        
    elif permission == constants.PERMISSION_COMMENT_REPLY:
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user == kwargs['author'].user
        )

def get_author_language_codes(author_id):
    language_codes = models.PostContent.objects.values('language_code').filter(
        post__author = author_id,
        post__status__gte=models.PostStatus.PUBLIC,
    ).distinct()
    return [code['language_code'] for code in list(language_codes)]

def get_post_language_codes(post_id):
    post_contents = models.PostContent.objects.filter(
        post = post_id,
        post__status__gte=models.PostStatus.PUBLIC,
    )
    return [post_content.language_code for post_content in post_contents]
