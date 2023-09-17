from django.urls import path
from apps.adverts.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('adverts/', # cache_page(60)
        (NewsList.as_view()), name='news_list'),
    path('adverts/<int:pk>', # cache_page(60 * 5)
        (NewsDetail.as_view()), name='new_detail'),
    path('', # cache_page(60)
        (NewsList.as_view())),  # default start with adverts page
    path('adverts/create/', NewCreate.as_view(), name='new_create'),
    path('adverts/<int:pk>/update', NewUpdate.as_view(), name='new_update'),
    path('adverts/<int:pk>/delete', NewDelete.as_view(), name='new_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/update', ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete', ArticleDelete.as_view(), name='article_delete'),
]