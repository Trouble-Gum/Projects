# Django portal

## Description
The program represents educational project including Skillfactory homework implementation

## Homeworks:
* Django flatpages
* News
* Sign

### Django flatpages
* https://localhost/
* https://localhost/about
* https://localhost/counterparties
* https://localhost/contacts/ (authorization is required)

### News
https://localhost/news  
Source: /apps/news  
Functionality represents usage of:
* Models
* Views
* Templates
* Tags and filters (/apps/news/templatetags/custom_filters.py)

## Sign
* source  
  https://localhost/accounts/login
  https://localhost/accounts/logout
  https://localhost/accounts/signup

  Functionality represents usage of Django classes and django-allauth library:
** django.shortcuts.redirect
** django.contrib.auth.models.Group
** django.contrib.auth.decorators.login_required
** django.contrib.auth.views.LoginView
** django.contrib.auth.views.LogoutView
** django.contrib.auth.forms.UserCreationForm
** allauth.account.forms.SignupForm

## Tech-stack:
* Python
* Django
* SQL
* HTML
* CSS

## RUN
launch python manage.py runserver and go to https://localhost/


