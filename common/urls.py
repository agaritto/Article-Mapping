from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
import polls
urlpatterns = [
    path('login/', polls.views.login),
    path('logout/', polls.views.login),
]