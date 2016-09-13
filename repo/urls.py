from django.conf.urls import url
from . import views

app_name = 'repo'
urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^home/$', views.home, name='home'),
	url(r'^library/$', views.library, name='library'),
	url(r'^login/$', views.login, name='login'),
	url(r'^register/$', views.register, name='register'),
	url(r'^results/?P<form>[A-Za-z]+/$', views.results, name='results'),
	url(r'^(?P<sn>[-\/\d\w]{5,100})/borrow/$', views.borrow, name='borrow'),
	#url(r'^(?P<sn>[.\D\d.]+)/borrow/$', views.borrow, name='borrow'),
]