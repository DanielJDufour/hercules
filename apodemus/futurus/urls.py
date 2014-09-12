from django.conf.urls.static import static
from django.conf.urls import include, url, patterns
from django.contrib import admin
from futurus import views
from django.conf import settings

urlpatterns = patterns(
    url(r'^$', views.index, name='index'),
    url(r'^find_organizations/', views.find_organizations, name='find_organizations'),
    url(r'^find_projects/', views.find_projects, name='find_projects'),
    url(r'^find_people/', views.find_people, name='find_people'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'orgs/(?P<slug>[^\.]+)', views.organization, name='organization'),
    url(r'projects/(?P<slug>[^\.]+)', views.project, name='project'),
    url(r'people/(?P<slug>[^\.]+)', views.person, name='person'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

