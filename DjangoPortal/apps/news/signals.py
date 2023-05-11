import sys

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import PostCategory, CategorySubscribers
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@receiver(m2m_changed, sender=PostCategory)
def post_category_handler(*args, **kwargs):
    if kwargs['action'] == 'post_add':

        categories = kwargs['pk_set']
        subscribers = CategorySubscribers.objects.filter(category_id__in=categories)
        subscribers = subscribers.values('subscriber__email', 'subscriber__username').distinct()

        mod = sys.modules['project.settings']

        for rec in subscribers:
            html_content = render_to_string(
                'news/post_created.html',
                {
                    'text': kwargs['instance'].text,
                    'username': rec["subscriber__username"],
                    'id': kwargs['instance'].id
                }
            )
            msg = EmailMultiAlternatives(
                subject=kwargs['instance'].caption,
                body=kwargs['instance'].text,
                from_email=f'{getattr(mod, "EMAIL_HOST_USER")}{getattr(mod, "EMAIL_POSTFIX")}',
                to=[rec['subscriber__email']]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
