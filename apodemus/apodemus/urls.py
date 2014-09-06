from django.conf.urls import include, url
from django.contrib import admin
import futurus

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', futurus.views.index, name='index'),
    url(r'^$', include(admin.site.urls)),
]
