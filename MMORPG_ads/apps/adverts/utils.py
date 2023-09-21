import sys

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email_after_new_comment(emails, title, text):
    #################################################################
    # Рассылка не тестировалась. Код условный. Практически псевдо-код
    #################################################################

    mod = sys.modules['project.settings']

    for rec in emails:
        html_content = render_to_string(
            'adverts/comment_created.html',
            {
                'text': text,
                'email': rec
            }
        )
        msg = EmailMultiAlternatives(
            subject=title,
            body=text,
            from_email=f'{getattr(mod, "EMAIL_HOST_USER")}{getattr(mod, "EMAIL_POSTFIX")}',
            to=[rec]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def send_emails_on_monday():
    pass
    ###############################################################################
    # Взял код из предыдущего проекта. Реализовать не успел. Но концепт аналогичный
    ###############################################################################

    # d = date.today() - timedelta(days=7)
    # posts = Post.objects.filter(posted_at__gte=d)
    # ctg = []
    # for rec in posts:
    #     categories = PostCategory.objects.filter(post=rec)
    #     for cat in categories:
    #         ctg.append(cat)
    # categories = set(ctg)  # for distinct values
    # subscribers = CategorySubscribers.objects.filter(category_id__in=categories)
    # subscribers = subscribers.values('subscriber__email', 'subscriber__username').distinct()
    #
    # mod = sys.modules['project.settings']
    #
    # for rec in subscribers:
    #     html_content = render_to_string(
    #         'adverts/weekly_emailing.html',
    #         {
    #             'text': 'Past week adverts in your favourite categories',
    #             'username': rec["subscriber__username"]
    #         }
    #     )
    #     msg = EmailMultiAlternatives(
    #         subject='Past week adverts in your favourite categories',
    #         body='Past week adverts in your favourite categories: ' + str(categories),
    #         from_email=f'{getattr(mod, "EMAIL_HOST_USER")}{getattr(mod, "EMAIL_POSTFIX")}',
    #         to=[rec['subscriber__email']]
    #     )
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()
