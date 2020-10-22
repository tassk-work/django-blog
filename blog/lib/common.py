from . import constants

def has_perm(request, permission, **kwargs):
    if permission == constants.PERMISSION_COMMENT_EDIT:
        return request.user.is_authenticated and request.user == kwargs['author'].user
        
    elif permission == constants.PERMISSION_COMMENT_REPLY:
        return request.user.is_authenticated and request.user == kwargs['author'].user
        