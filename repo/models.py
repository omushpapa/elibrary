from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models.signals import post_delete, pre_delete
from django.dispatch.dispatcher import receiver
#from repo.forms import UserForm

# @python_2_unicode_compatible
class UserData(models.Model):
	username = models.CharField(max_length=15)
	password = models.CharField(max_length=255)
	email = models.CharField(max_length=30)
	USER_LEVEL = (
			('admin', 'Admin'),
			('staff', 'Staff'),
			('hof', 'Head of Facilities'),
			('user', 'User'),
		)
	user_level = models.CharField(max_length=7, choices=USER_LEVEL, default='user')

	def __unicode__(self):
		return unicode(self.username)

class BookCategory(models.Model):
	category_name = models.CharField(max_length=40, blank=True, default='Unknown')

	def __unicode__(self):
		return unicode(self.category_name)

class BookAuthors(models.Model):
	author_first_name = models.CharField(max_length=25, blank=True)
	author_last_name = models.CharField(max_length=25, blank=False, default='Unknown')
	author_middle_name = models.CharField(max_length=25, blank=True)

	def __unicode__(self):
		return unicode(self.author_last_name)

class LibraryBook(models.Model):
	book_title = models.CharField(max_length=100, blank=False)
	book_author_id = models.ForeignKey(BookAuthors, on_delete=models.CASCADE)
	category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
	quantity = models.IntegerField(blank=False, default=0)
	number_borrowed = models.IntegerField(default=0)

	def __unicode__(self):
		return unicode(self.book_title)

class SingleBook(models.Model):
	serial_number = models.CharField(primary_key=True , max_length=150, blank=False)
	book_id = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
	is_available_returned = models.BooleanField(default=True)
	#is_borrowed = models.BooleanField(default=False)

	def __unicode__(self):
		return unicode(self.book_id)

class BorrowingLog(models.Model):
	comment = models.CharField(max_length=30, blank=False)
	log_name = models.ForeignKey(SingleBook, on_delete=models.CASCADE)
	bookid = models.ForeignKey(LibraryBook, on_delete=models.CASCADE, related_name='book', related_query_name='log')
	userid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='log_user', related_query_name='log')
	lend_date = models.DateField()
	expected_return_date = models.DateField()
	surchages = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=0.00)

	def __unicode__(self):
		return unicode(str(self.bookid) + " - " + str(self.log_name) + " -- " + str(self.comment))

@receiver(post_delete, sender=SingleBook)
def singlebook_deleted(sender, instance, **kwargs):
	instance.book_id.quantity -= 1
	if not instance.is_available_returned:
		instance.book_id.number_borrowed -= 1
	instance.book_id.save()