from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from apps.sign.views import BaseRegisterView, upgrade_me
from apps.sign.forms import activate_user_account

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='sign/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name='sign/signup.html'),
         name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path(r'^activate/(?P[0-9A-Za-z_\-]+)/(?P[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/account/$',
         activate_user_account, name='activate_user_account')
]
