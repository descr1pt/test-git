from celery import shared_task
import datetime
import time
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from django.conf import settings
from .models import Post, Category


# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")
#
#
# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)


@shared_task
def send_notifications(pk):
    post = Post.objects.get(pk=pk)
    categories = post.postCategory.all()
    title = post.title
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.preview,
            'link': f'http://127.0.0.1:8000/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_mailing():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    this_week_posts = Post.objects.filter(creationDate__gt=last_week)
    for category in Category.objects.all():
        post_list = this_week_posts.filter(postCategory=category)
        if post_list:
            subscribers = category.subscribers.values('username', 'email')
            recipients = []
            for subscriber in subscribers:
                recipients.append(subscriber['email'])

            html_content = render_to_string(
                'news/daily_news.html',
                {
                    'link': f'{settings.SITE_URL}news/',
                }
            )

            msg = EmailMultiAlternatives(
                subject='Статьи за неделю',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipients,
            )

            msg.attach_alternative(html_content, 'text/html')
            msg.send()

    print('Рассылка произведена!')