from django.views.generic import ListView, DetailView

from apps.news.models import Post


class NewsList(ListView):
    model = Post
    ordering = '-posted_at'
    template_name = 'news.html'
    context_object_name = 'news'


class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
