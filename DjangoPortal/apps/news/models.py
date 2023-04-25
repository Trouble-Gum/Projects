from django.db import models
from django.contrib.auth.models import User
from django.db.models.manager import Manager
from django.core.exceptions import *
from django.urls import reverse


# Create your models here.

class Author(models.Model):
    """Django model which implements Author entity"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    objects = Manager()

    def update_rating(self):
        """
        Reckons authors rating based on posts/comments and puts total sum into DB
        """
        total_rating = 0
        for rec in Post.objects.filter(author=self):
            total_rating += rec.rating * 3
            # print(rec.rating)
            for com in Comment.objects.filter(post=rec):
                total_rating += com.rating
                # print('   ', com.rating)
        for com in Comment.objects.filter(user=self.user):
            total_rating += com.rating
            # print(' ', com.rating)
        self.rating = total_rating
        self.save()

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


class Category(models.Model):
    """Django model which implements Category entity"""
    objects = Manager()
    category_name = models.CharField(max_length=20, unique=True)


article = 'AR'
new = 'NE'

POST_TYPES = [
    (article, 'Article'),
    (new, 'New')
]


class Post(models.Model):
    """Django model which implements Post entity"""
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=new)
    posted_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    caption = models.CharField(max_length=100)
    text = models.CharField(max_length=10000)
    rating = models.FloatField(default=0)

    objects = Manager()

    def like(self, username=''):  # storing information about likes-history are supposed in future
        """increases amount of posts likes"""
        self.rating += 1
        self.save()

    def dislike(self, username=''):  # storing information about dislikes-history are supposed in future
        """decreases amount of post likes"""
        self.rating -= 1
        self.save()

    def preview(self):
        """returns first 124 letters of post text"""
        return self.text[:124] + '...' if len(str(self.text)) > 124 else self.text

    def __str__(self):
        return f'{self.caption}: {self.preview()}'

    @property
    def author_name(self):
        return self.author.get_username()

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.pk)])


class PostCategory(models.Model):
    """Django model which implements many-to-many relationship between entities (Post&Category)"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """Django model which implements Comment entity"""
    objects = Manager()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=1000)
    commented_at = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)

    def like(self, username=''):  # storing information about likes-history are supposed in future
        """increases amount of comment likes"""
        self.rating += 1
        self.save()

    def dislike(self, username=''):  # storing information about dislikes-history are supposed in future
        """decreases amount of post likes"""
        self.rating -= 1
        self.save()
