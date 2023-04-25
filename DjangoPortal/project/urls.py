"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from project import views
from apps.news import views as news_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('counterparties/', views.CounterpartiesTable.as_view()),
    path('news/', news_views.NewsList.as_view(), name='news_list'),
    path('news/<int:pk>', news_views.NewsDetail.as_view(), name='new_detail'),
    path('', news_views.NewsList.as_view()),  # default start with news page
    path('news/create/', news_views.NewCreate.as_view(), name='new_create'),
    path('news/<int:pk>/update', news_views.NewUpdate.as_view(), name='new_update'),
    path('news/<int:pk>/delete', news_views.NewDelete.as_view(), name='new_delete'),
    path('articles/create/', news_views.ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/update', news_views.ArticleUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete', news_views.ArticleDelete.as_view(), name='article_delete'),
]
