from celery import shared_task
from .models import Post, CategorySubscribers
from .utils import send_email_after_new_post, send_emails_on_monday


@shared_task
def complete_order(pid):
    post = Post.objects.get(pk=pid)
    categories = post.categories
    subscribers = CategorySubscribers.objects.filter(category_id__in=categories)
    subscribers = subscribers.values('subscriber__email', 'subscriber__username').distinct()
    send_email_after_new_post(subscribers, post.caption, post.text, post.pk)
    # post.save()


@shared_task
def monday_emailing():
    send_emails_on_monday()
