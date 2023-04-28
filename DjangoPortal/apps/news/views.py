from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from apps.news.models import Post, article, new
from apps.news.filters import PostFilter
from apps.news.forms import NewForm, NewArticle


class NewsList(ListView):
    model = Post
    ordering = '-posted_at'
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def __init__(self):
        super().__init__()
        self.filter_set = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_set = PostFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_set'] = self.filter_set
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/new.html'
    context_object_name = 'new'


def get_context_data_(self, **kwargs):
    context = None
    if isinstance(self, View) and hasattr(self, 'post_type'):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['post_type'] = self.__getattribute__('post_type')
    return context


class NewCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = NewForm
    model = Post
    template_name = 'news/new_edit.html'
    post_type = 'New'
    get_context_data = get_context_data_

    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = new
        return super().form_valid(form)


class NewUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = NewForm
    model = Post
    template_name = 'news/new_edit.html'
    post_type = 'New'
    get_context_data = get_context_data_

    permission_required = ('news.change_post',)


class NewDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/new_delete.html'
    success_url = reverse_lazy('news_list')
    post_type = 'New'
    get_context_data = get_context_data_

    permission_required = ('news.delete_post',)


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = NewArticle
    model = Post
    template_name = 'news/new_edit.html'
    post_type = 'Article'
    get_context_data = get_context_data_

    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = article
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = NewArticle
    model = Post
    template_name = 'news/new_edit.html'
    post_type = 'Article'
    get_context_data = get_context_data_

    permission_required = ('news.change_post',)


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/new_delete.html'
    success_url = reverse_lazy('news_list')
    post_type = 'Article'
    get_context_data = get_context_data_

    permission_required = ('news.delete_post',)
