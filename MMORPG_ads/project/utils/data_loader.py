from random import *
from django.db.models.query import QuerySet

from apps.adverts.models import *

u1 = User.objects.create_user(username='username1')
u2 = User.objects.create_user(username='username2')

a1 = Author.create_author('MusicReviewer', 'qwerty123456')
a2 = Author.create_author('FilmReviewer', 'qwerty123456')

Category(category_name='Music').save()
Category(category_name='Journals').save()
Category(category_name='Films').save()
Category(category_name='History').save()
Category(category_name='Cars').save()

p = Post(author=Author.get_author('MusicReviewer'),
         post_type=new,
         caption='New Rolling Stones rating',
         text='There could be the place for your advertisement'
         )
p.save()
p.categories.set([Category.objects.get(category_name=rec) for rec in ['Music', 'Journals']])

p = Post(author=Author.get_author('FilmReviewer'),
         post_type=article,
         caption='About IMDB critics',
         text='There could be the place for your advertisement'
         )
p.save()
p.categories.set([Category.objects.get(category_name=rec) for rec in ['Films', 'History']])

p = Post(author=Author.get_author('FilmReviewer'),
         post_type=article,
         caption='History of the film "In Bruges" by Martin McDonagh',
         text='There could be the place for your advertisement'
         )
p.save()
p.categories.set([Category.objects.get(category_name=rec) for rec in ['History', 'Cars']])

post_reactions = {1: Post.like, 2: Post.dislike}
users = User.objects.all()
comment_reactions = {1: Comment.like, 2: Comment.dislike}


def do_reaction(obj, dict_):
    for i in range(len(users)):
        usr = choice(users)
        react = dict_[choice(list(dict_.keys()))]
        react(obj, username=usr.username)


for rec in Post.objects.all():
    do_reaction(rec, post_reactions)

    cmt = Comment(
        post=rec,
        user=u1,
        text=f'comment by {u1.username}'
    )
    cmt.save()
    do_reaction(cmt, comment_reactions)

    cmt = Comment(
        post=rec,
        user=u2,
        text=f'comment by {u2.username}'
    )
    cmt.save()
    do_reaction(cmt, comment_reactions)

    cmt = Comment(
        post=rec,
        user_id=a1.user_id,
        text=f'comment by {a1.get_username()}'
    )
    cmt.save()
    do_reaction(cmt, comment_reactions)

    cmt = Comment(
        post=rec,
        user_id=a2.user_id,
        text=f'comment by {a2.get_username()}'
    )
    cmt.save()
    do_reaction(cmt, comment_reactions)


list(map(Author.update_rating, Author.objects.all()))

a1 = Author.get_author('MusicReviewer')
a2 = Author.get_author('FilmReviewer')

a1.update_rating()
a2.update_rating()

qs: QuerySet = Author.objects.all().order_by('-rating').values('user__username', 'rating')
leader = qs.first()
print(f'Top rated author: \n  {leader["user__username"]} \n  rating: {leader["rating"]} \n')

qs = Post.objects.all().order_by('-rating').values('id', 'posted_at', 'rating', 'author__user__username')
leader = qs.first()
print(f'Top rated post: \n  {leader["posted_at"].strftime("%d.%m.%Y %H:%M:%S")} \n  rating: {leader["rating"]} \n  '
      f'author: {leader["author__user__username"]} \n  '
      f'preview: {Post.objects.get(id=leader["id"]).preview()} \n')

comments = Comment.objects.filter(post_id=leader['id']).values('commented_at', 'user__username', 'rating', 'text')
comments = list(comments)
list(map(print, [f'comment: {rec["text"]} \n    commented_at: {rec["commented_at"].strftime("%d.%m.%Y %H:%M:%S")} \n'
                 f'    username: {rec["user__username"]} \n    rating: {rec["rating"]} \n'
                 for rec in comments]))

# D7.7 Final module project

user = User.objects.create_user("TechReviewer", "", "x")
user.save()


exit()
