from django.conf.urls.static import static
from django.conf.urls import include, url, patterns
from django.contrib import admin
from futurus import views
from django.conf import settings
import futurus

urlpatterns = patterns(
    url(r'^futurus/', include('futurus.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^account$', views.account, name='account'),
    url(r'^advise$', views.advise, name='advise'),
    url(r'^browse_organizations$', views.browse_organizations, name='browse_organizations'),
    url(r'^browse_people/', views.browse_people, name='browse_people'),
    url(r'^browse_projects/', views.browse_projects, name='browse_projects'),
    url(r'^change_language$', views.change_language, name='change_language'),
    url('^create_organization$', views.create_organization, name='create_organization'),
    url('^create_profile$', views.create_person, name='create_person'),
    url('^create_project$', views.create_project, name='create_project'),
    url('^json/organizations$', views.json_organizations, name='json_organizations'),
    url('^my_donations$', views.transactions, name='transactions'),
    url(r'people/(?P<slug>[^\./]+)/edit$', views.edit_person, name='edit_person'),
    url(r'people/(?P<slug>[^\./]+)/memberships$', views.memberships, name='memberships'),
    url(r'^find_organizations/', views.find_organizations, name='find_organizations'),
    url(r'^find_projects/', views.find_projects, name='find_projects'),
    url(r'^find_people/', views.find_people, name='find_people'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'orgs/(?P<slug>[^\./]+)$', views.organization, name='organization'),
    url(r'orgs/(?P<slug>[^\./]+)/edit$', views.edit_organization, name='edit_organization'),
    url(r'projects/(?P<slug>[^\.]+)', views.project, name='project'),
    url(r'people/(?P<slug>[^\.]+)', views.person, name='person'),
    url(r'register/', views.register, name='register'),
    url(r'login/$', views.user_login, name='login'),
    url(r'logout/', views.user_logout, name='logout'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^tasks$', views.tasks, name='tasks'),
    url(r'^translate$', views.translate, name='translate'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
"""

