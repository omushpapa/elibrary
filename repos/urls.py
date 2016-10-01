from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
from django.http import HttpResponseRedirect

urlpatterns = [
    url(r'^$', lambda u: HttpResponseRedirect('/reg')),
	url(r'^controller/logout/$', views.logout, {'next_page': '/repo/home/'}),
    url(r'^controller/', admin.site.urls),
    url(r'^repo/', include('repo.urls')),
    url(r'^reg/', include('reg.urls')),
    url(r'^tracker/', include('tracker.urls')),
    url(r'^todos/', include('todo.urls')),
]
