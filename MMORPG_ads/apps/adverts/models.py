from django.db import models
from django.contrib.auth.models import User
from django.db.models.manager import Manager
from django.core.exceptions import *
from django.urls import reverse
from django.core.cache import cache

from django.db import models
from martor.models import MartorField

from apps.adverts.middleware import get_current_user

# Create your models here.


class Author(models.Model):
    """Django model which implements Author entity"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)
    name: str
    objects = Manager()

    @staticmethod
    def create_author(username, password, user_id=None):
        """ Constructor for Author-instance
            :param str username: username or author (related Built-in entity User)
            :param str password: password or author (related Built-in entity User)
            :param int user_id: users UID
            :return: instance of created Author
            :rtype: Author
        """
        if not user_id:
            u = User.objects.create_user(username=username, password=password)
            user_id = u.pk
        else:
            user_id = user_id
            u = None
        try:
            au = Author.objects.create(user_id=user_id)
        except Exception as e:
            print('An error occurred during initializing the new author in DB - ' + str(e))
            # print will be replaced with logging later
            if u:
                try:
                    u.delete()
                except Exception as e:
                    raise f"The data is inconsistent. No author matches new user with id = {user_id}" \
                          f"Delete user manually if need. Exception: {str(e)}"
            au = None
        else:
            au.save()
        return au

    @staticmethod
    def get_author(*args, **kwargs):
        """returns author matched passed params (username or email)
        variants of usage: get_author('your_login'), get_author(username='your_login'),
        get_author(email='your_email')
        """
        try:
            if args[0]:
                result = Author.objects.get(user__username=args[0])
            elif 'username' in kwargs.keys():
                result = Author.objects.get(user__username=kwargs['username'])
            elif 'email' in kwargs.keys() and kwargs['email'] and kwargs['email'] != '':
                result = Author.objects.get(user__email=kwargs['email'])
            else:
                result = Author.objects.get(**kwargs)
        except models.ObjectDoesNotExist:
            result = None
        except MultipleObjectsReturned:
            raise MultipleObjectsReturned(f'Returned more than one Author. Passed params: {kwargs}')
        return result

    def get_username(self):
        """returns username of Author instance"""
        result = Author.objects.filter(pk=self.pk).values('user__username')
        result = result[0]['user__username']
        return result

    def __str__(self):
        user_: User = User.objects.get(pk=self.__getattribute__('user_id'))
        result = f'{user_.last_name} {user_.first_name}'
        return result if result.strip() else self.get_username()


tnk = 'tnk'
hl = 'hl'
dd = 'dd'
trd = 'trd'
gm = 'gm'
qst = 'qst'
bsm = 'bsm'
skn = 'skn'
zlv = 'zlv'
mst = 'mst'

POST_CATEGORIES = [
    (tnk, 'Танки'),
    (hl, 'Хилы'),
    (dd, 'ДД'),
    (trd, 'Торговцы'),
    (gm, 'Гилдмастеры'),
    (qst, 'Квестгиверы'),
    (bsm, 'Кузнецы'),
    (skn, 'Кожевники'),
    (zlv, 'Зельевары'),
    (mst, 'Мастера заклинаний')
]


class Post(models.Model):
    """Django model which implements Post entity"""
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, default=get_current_user())
    post_type = models.CharField(max_length=30, choices=POST_CATEGORIES, default=tnk)
    posted_at = models.DateTimeField(auto_now_add=True)

    caption = models.CharField(max_length=100)

    description = MartorField(default='Type your text here')

    objects = Manager()

    def preview(self):
        """returns first 124 letters of post text"""
        return self.text[:124] + '...' if len(str(self.text)) > 124 else self.text

    def __str__(self):
        return f'{self.caption}: {self.preview()}'

    @property
    def author_name(self):
        return self.author.get_username()

    def get_absolute_url(self):
        return reverse('advert_detail', args=[str(self.pk)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class Reply(models.Model):
    """Django model which implements Comment entity"""
    objects = Manager()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=1000)
    commented_at = models.DateTimeField(auto_now_add=True)



