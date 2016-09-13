from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class TodoList(models.Model):
	todo_name = models.CharField(max_length=100, blank=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	card = models.ManyToManyField('Card', blank=True, related_name='card_list')
	PUBLICITY_STATUS = (
			('private', 'Private'),
			('public', 'Public'),
		)
	publicity_status = models.CharField(max_length=8, choices=PUBLICITY_STATUS, default='private')

	class Meta:
		ordering = ['todo_name']

	def __unicode__(self):
		return unicode(self.todo_name)

class Card(models.Model):
	card_name = models.CharField(max_length=25, blank=False)
	todo_item = models.ManyToManyField('TodoItem', blank=True, related_name='items_card')
	description = models.CharField(max_length=50, blank=True)

	class Meta:
		ordering = ['card_name']

	def __unicode__(self):
		return unicode(self.card_name)

class TodoItem(models.Model):
	item_name = models.CharField(max_length=25, blank=False)
	item_description = models.CharField(max_length=200)
	STATUS = (
			('private', 'Private'),
			('public', 'Public'),
		)
	status = models.CharField(max_length=8, choices=STATUS, default='private')
	is_done = models.BooleanField(default=False)

	class Meta:
		ordering = ['item_name']

	def __unicode__(self):
		return unicode(self.item_name)