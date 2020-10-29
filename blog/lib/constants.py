import enum

SESSION_MESSAGES = 'SESSION_MESSAGES'

OPERATION_LOG = 'blog.operation'

PERMISSION_COMMENT_EDIT = 'comment_edit'
PERMISSION_COMMENT_REPLY = 'comment_reply'

class AuthorFlag(enum.Enum):
    COMMENT_FLAG = 1 << 0

class PostFlag(enum.Enum):
    COMMENT_FLAG = 1 << 0
