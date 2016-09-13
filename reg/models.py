from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible


class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='user', related_query_name='userp')
	photo = models.FileField(upload_to=(
					"main.UserProfile.photo", "profiles"),
					max_length=255, null=True, blank=True
				)
	website = models.URLField(default='', blank=True)
	bio = models.TextField(default='', blank=True)
	phone = models.CharField(max_length=20, default='', blank=True)
	city = models.CharField(max_length=20, default='', blank=True)
	country = models.CharField(max_length=25, default='', blank=True)
	organisation = models.CharField(max_length=50, default='', blank=True)

	def __unicode__(self):
		return unicode(self.user)

def create_profile(sender, **kwargs):
	user = kwargs["instance"]
	if kwargs["created"]:
		user_profile = UserProfile(user=user)
		user_profile.save()
post_save.connect(create_profile, sender=User)