from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext as _

# codestart:comment_notification
def comment_notification(request, comment):
    if not comment.blog.author.user.email:
        return
    subject = _('COMMENT_NOTIFICATION_SUBJECT').format(comment.blog.author.title_text)
    context = {
        'comment': comment,
        'url': request.build_absolute_uri(reverse('blog:detail', args=[comment.blog.author.user.username, comment.blog.id])),
    }
    message = render_to_string('blog/mails/comment_notification.txt', context, request)
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [comment.blog.author.user.email] 
    send_mail(subject, message, from_email, recipient_list)
# codeend:comment_notification