from futurus import views
from django.conf.urls import patterns, include, url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('find', views.find, name='find'),
]
