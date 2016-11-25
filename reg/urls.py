from django.conf.urls import url, include
from . import views
from django.contrib import auth

app_name = 'reg'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^home/$', views.home, name='home'),
	url(r'^index/$', views.home, name='index'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.login_user, name='login'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^password/change/alter/$', auth.views.password_change, {
		'template_name': 'reg/pass_change.html', 
		'post_change_redirect': '/repo/home'
		}, name='password_change'),
	url(r'^(?P<pk>[\w\d]+)/profile/$', views.edit_user, name='edit_user'),
	url(r'^(?P<pk>[\w\d]+)/viewprofile/$', views.profile, name='profile'),
]