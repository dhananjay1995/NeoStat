
from django.conf.urls import url, include
from django.contrib import admin
from . import views

app_name = 'NeoApp'


urlpatterns = [
    url(r'^$', views.Index, name="Index"),
    url(r'^searchAPI/$', views.searchAPI, name="searchAPI"),
]
