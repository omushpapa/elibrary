from django.conf.urls import include, url
from . import views

app_name = 'todo'
urlpatterns = [
	url(r'^lists/$', views.todolists, name='todo_lists'),
	url(r'^lists/(?P<list_id>[\w\d]+)/update/$', views.UpdateTodoList.as_view(), name='update_list'),
	url(r'^lists/card/(?P<card_id>[\w\d]+)/$', views.cards, name='cards'),
	url(r'^lists/new/$', views.CreateList.as_view(), name='new_list'),
	url(r'^lists/card/new/(?P<list_id>[\w\d]+)/$', views.CreateCard.as_view(), name='new_card'),
	url(r'^lists/card/(?P<card_id>[\w\d]+)/update/$', views.UpdateCard.as_view(), name='update_card'),
	url(r'^lists/card/(?P<card_id>[\w\d]+)/move/$', views.move_card, name='move_card'),
	url(r'^lists/card/(?P<card_id>[\w\d]+)/items/new/$', views.CreateTodoItem.as_view(), name='new_item'),
	url(r'^lists/card/(?P<item_id>[\w\d]+)/items/update/$', views.UpdateTodoItem.as_view(), name='update_item'),
]