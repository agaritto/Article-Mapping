from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from polls import views as polls_views



urlpatterns = [
    path('', polls_views.index),
    path('doi/', polls_views.doi),
    path('doi/relation/', polls_views.relation),
    path('test/', polls_views.test),
    path('neo4jwork/', polls_views.neo4jwork),
    path('login/', polls_views.login),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('aura_nodeinput/', polls_views.aura_nodeinput),
    path('aura_relationinput/', polls_views.aura_relationinput),
    path('desktop_nodeinput/', polls_views.desktop_nodeinput),
    path('desktop_relationinput/', polls_views.desktop_relationinput),
    path('relationdb/', polls_views.relationcreatedb),
]