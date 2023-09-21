from django.urls import path
from apps.adverts.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('adverts/', # cache_page(60)
        (AdvertsList.as_view()), name='adverts_list'),
    path('adverts/<int:pk>', # cache_page(60 * 5)
        (AdvertDetail.as_view()), name='advert_detail'),
    path('', # cache_page(60)
        (AdvertsList.as_view())),  # default start with adverts page
    path('adverts/create/', AdvertCreate.as_view(), name='advert_create'),
    path('adverts/<int:pk>/update', AdvertUpdate.as_view(), name='advert_update'),
    path('adverts/<int:pk>/delete', AdvertDelete.as_view(), name='advert_delete'),
]