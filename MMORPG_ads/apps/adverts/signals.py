from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.adverts.models import Reply
from apps.adverts.utils import send_email_after_new_comment


@receiver(pre_save, sender=Reply)
def comment_handler(*args, **kwargs):
    if kwargs['action'] == 'comment_add':
        pass
# ТУТ НУЖНО РЕАЛИЗОВАТЬ ЛОГИКУ ПОИСКА ПОЧТЫ АВТОРА ПОСТА НА КОТОРЫЙ СОЗДАЕТСЯ КОММЕНТ
# И ОТПРАВИТЬ АВТОРУ
# # send_email_after_new_comment()
