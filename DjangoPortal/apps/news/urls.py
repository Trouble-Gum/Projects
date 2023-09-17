from django.urls import path
from apps.news.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('news/', # cache_page(60)
        (NewsList.as_view()), name='news_list'),
    path('news/<int:pk>', # cache_page(60 * 5)
        (NewsDetail.as_view()), name='new_detail'),
    path('', # cache_page(60)
        (NewsList.as_view())),  # default start with news page
    path('news/create/', NewCreate.as_view(), name='new_create'),
    path('news/<int:pk>/update', NewUpdate.as_view(), name='new_update'),
    path('news/<int:pk>/delete', NewDelete.as_view(), name='new_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/update', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
]