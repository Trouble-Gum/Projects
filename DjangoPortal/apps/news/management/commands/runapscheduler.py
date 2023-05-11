import sys
from datetime import date, timedelta

import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.news.models import Post, PostCategory, CategorySubscribers

logger = logging.getLogger(__name__)


def my_job():
    #  Your job processing logic here...
    d = date.today() - timedelta(days=7)
    posts = Post.objects.filter(posted_at__gte=d)
    ctg = []
    for rec in posts:
        categories = PostCategory.objects.filter(post=rec)
        for cat in categories:
            ctg.append(cat)
    categories = set(ctg)  # for distinct values
    subscribers = CategorySubscribers.objects.filter(category_id__in=categories)
    subscribers = subscribers.values('subscriber__email', 'subscriber__username').distinct()

    mod = sys.modules['project.settings']

    for rec in subscribers:
        html_content = render_to_string(
            'news/weekly_emailing.html',
            {
                'text': 'Past week news in your favourite categories',
                'username': rec["subscriber__username"]
            }
        )
        msg = EmailMultiAlternatives(
            subject='Past week news in your favourite categories',
            body='Past week news in your favourite categories: ' + str(categories),
            from_email=f'{getattr(mod, "EMAIL_HOST_USER")}{getattr(mod, "EMAIL_POSTFIX")}',
            to=[rec['subscriber__email']]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
