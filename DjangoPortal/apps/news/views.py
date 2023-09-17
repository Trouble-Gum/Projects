from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.core.handlers.wsgi import WSGIRequest
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.news.models import Post, article, new, CategorySubscribers, Category
from apps.news.filters import PostFilter
from apps.news.forms import NewForm, NewArticle
from .tasks import complete_order


class NewsList(ListView):
    model = Post
    ordering = '-posted_at'
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def __init__(self):
        super().__init__()
        self.category_filter_values = None
        self.filter_set = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_set = PostFilter(self.request.GET, queryset)
        return self.filter_set.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_set'] = self.filter_set
        context['category_filter_values'] = self.category_filter_values
        return context

    def get(self, request: WSGIRequest, *args, **kwargs):
        req = dict(request.GET)
        try:
            self.category_filter_values = req['category']
        except KeyError as e:
            self.category_filter_values = None
            # print(f'No category passed {e}')  # will be replaced with logging later

        try:
            subscribe = req['subscribe'][0]

            if subscribe == 'subscribe':

                for rec in req['category']:
                    try:
                        cs = CategorySubscribers(subscriber=request.__getattribute__('user'),
                                                 category=Category.objects.get(category_name=rec)
                                                 )
                        cs.save()
                    except (IntegrityError, ObjectDoesNotExist):  # cases of user are still subscribed on category
                        # or chose "None"
                        pass
        except KeyError as e:
            pass

        return super().get(self, request, *args, **kwargs)

    # def post(self, request: WSGIRequest, *args, **kwargs):
    #     post = dict(request.POST)
    #     # context = super().get_context_data(**kwargs)
    #     if post['subscribe'] == ['subscribe']:
    #         print('RQ - ' + str(request.GET))
    #         # for rec in self.category_filter_values:
    #         #     print(rec)
    #         # cs = CategorySubscribers(subscriber=request.user, category=Category.objects.get(category_name='Cars'))
    #         # cs.save()
    #     return redirect('/')


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/new.html'
    context_object_name = 'new'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


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
        # print(form)
        post = form.save(commit=False)
        post.post_type = new
        complete_order.apply_async([post.pk], countdown=10)
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
