from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.core.handlers.wsgi import WSGIRequest
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from apps.adverts.models import Post
from apps.adverts.filters import PostFilter
from apps.adverts.forms import NewForm

from apps.adverts.middleware import get_current_user


class AdvertsList(ListView):
    model = Post
    ordering = '-posted_at'
    template_name = 'adverts/adverts.html'
    context_object_name = 'adverts'
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


class AdvertDetail(DetailView):
    model = Post
    template_name = 'adverts/advert.html'
    context_object_name = 'advert'

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


class AdvertCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = NewForm
    model = Post
    template_name = 'adverts/advert_edit.html'
    post_type = 'Advert'
    get_context_data = get_context_data_
    usr = get_current_user()
    permission_required = ('adverts.add_post',)

    def form_valid(self, form):
        # print(form)
        post = form.save(commit=False)
        # complete_order.apply_async([post.pk], countdown=10)
        return super().form_valid(form)


class AdvertUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = NewForm
    model = Post
    template_name = 'adverts/advert_edit.html'
    post_type = 'Advert'
    get_context_data = get_context_data_

    permission_required = ('adverts.change_post',)


class AdvertDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'adverts/advert_delete.html'
    success_url = reverse_lazy('adverts_list')
    post_type = 'Advert'
    get_context_data = get_context_data_

    permission_required = ('adverts.delete_post',)
