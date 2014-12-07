from django.conf.urls.static import static
from django.conf.urls import include, url, patterns
from django.contrib import admin
from futurus import views
from django.conf import settings
import futurus

urlpatterns = patterns(
    url(r'^futurus/', include('futurus.urls')),
    url(r'^$', views.index, name='index'),
    url('^create_organization$', views.create_organization, name='create_organization'),
    url(r'people/(?P<slug>[^\./]+)/edit$', views.edit_person, name='edit_person'),
    url(r'people/(?P<slug>[^\./]+)/memberships$', views.memberships, name='memberships'),
    url(r'^find_organizations/', views.find_organizations, name='find_organizations'),
    url(r'^find_projects/', views.find_projects, name='find_projects'),
    url(r'^find_people/', views.find_people, name='find_people'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'orgs/(?P<slug>[^\.]+)', views.organization, name='organization'),
    url(r'projects/(?P<slug>[^\.]+)', views.project, name='project'),
    url(r'people/(?P<slug>[^\.]+)', views.person, name='person'),
    url(r'register/', views.register, name='register'),
    url(r'login/$', views.user_login, name='login'),
    url(r'logout/', views.user_logout, name='logout'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^tasks$', views.tasks, name='tasks'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
"""

