import sys

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import PostCategory, CategorySubscribers
from .utils import send_email_after_new_post


@receiver(m2m_changed, sender=PostCategory)
def post_category_handler(*args, **kwargs):
    pass  # emailing is moved to tasks.py -> complete_order
    # if kwargs['action'] == 'post_add':
    #
    #     categories = kwargs['pk_set']
    #     subscribers = CategorySubscribers.objects.filter(category_id__in=categories)
    #     subscribers = subscribers.values('subscriber__email', 'subscriber__username').distinct()
    #
    #     send_email_after_new_post(subscribers, kwargs['instance'].title,
    #                               kwargs['instance'].text, kwargs['instance'].id)
