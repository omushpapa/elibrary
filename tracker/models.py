from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, pre_save
from django.core.mail import EmailMultiAlternatives, EmailMessage, send_mail
from django.core.validators import RegexValidator

class Issue(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_user')
	handler = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_handler', 
		default=User.objects.filter(username='admin')[0].id)
	issue_name = models.CharField(max_length=25, blank=False)
	description = models.CharField(max_length=100, blank=False)
	time_raised = models.DateTimeField(default=timezone.now)
	PRIORITY = (
			('low', 'Low'),
			('medium', 'Medium'),
			('high', 'High'),
		)
	priority = models.CharField(max_length=7, choices=PRIORITY, default='low')
	STATUS = (
			('in_progress', 'In Progress'),
			('resolved', 'Resolved'),
		)
	status = models.CharField(max_length=12, choices=STATUS, default='in-progress')
	time_resolved = models.DateTimeField(default=timezone.now)
	comments = models.CharField(max_length=255, default='', blank=True)
	is_seen = models.BooleanField(default=False)

	def __unicode__(self):
		return unicode(self.issue_name)

class Notification(models.Model):
	user_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name='notification_to')
	note = models.CharField(max_length=255)
	note_time = models.DateTimeField(default=timezone.now)

	def __unicode__(self):
		return unicode(self.note)

class Maintenance(models.Model):
	request_name = models.CharField(max_length=25)
	requested_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_user')
	maintainer = models.ManyToManyField('Maintainer', default=User.objects.filter(username='admin')[0].id, blank=True, related_name='maintainer')
	description = models.CharField(max_length=200)
	time_requested = models.DateTimeField(default=timezone.now)
	APPROVAL_STATUS = (
			('approved', 'Approved'),
			('rejected', 'Rejected'),
		)
	approval_status = models.CharField(max_length=10, choices=APPROVAL_STATUS, null=True, blank=True)
	PROGRESS = (
			('in-progress', 'In Progress'),
			('resolved', 'Resolved'),
		)
	progress = models.CharField(max_length=12, choices=PROGRESS, default='in-progress')
	time_resolved = models.DateTimeField(default=timezone.now)
	comments = models.CharField(max_length=150, default='', blank=True)
	#photo = models.URLField(max_length=200)
	is_seen = models.BooleanField(default=False)

	def __unicode__(self):
		return unicode(self.request_name)

class Maintainer(models.Model):
	contact_regex = RegexValidator(regex=r'^\+?1?\d{9,15}', message='Phone number must be in the format +123456789 (from 9 to 15 digits).')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	#maintenance = models.ForeignKey(Maintenance, on_delete=models.CASCADE, related_name='maintenance')
	contact = models.CharField(validators=[contact_regex], max_length=16)

	def __unicode__(self):
		return unicode(self.user)

class Document(models.Model):
	title = models.CharField(max_length=60)
	url = models.URLField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	document_category = models.ForeignKey('DocumentCategory', on_delete=models.PROTECT)
	#keyword = models.CharField(max_length=100)

	def __unicode__(self):
		return unicode(self.title)

class DocumentCategory(models.Model):
	category_name = models.CharField(max_length=50)

	def __unicode__(self):
		return unicode(self.category_name)

@receiver(pre_save, sender=Issue)
def issue_resolved(sender, instance, **kwargs):
	if instance.status == 'resolved' or instance.comments:
		instance.time_resolved = timezone.now()
		instance.is_seen = True

@receiver(post_save, sender=Issue)
def issue_update(sender, instance, **kwargs):
	if kwargs['created']:
		subject = 'Issue Raised'
		from_email = 'sterappdev@gmail.com'
		to = instance.user.email
		text_content = 'An issue has been raised on your site. Fulfill your responsibilities as admin.'
		#email = EmailMessage(subject, text_content, from_email, [to],)
		#email.send()
		send_mail(subject, text_content, from_email, [to])

	if instance.status == 'resolved':
		message = 'Your issue, %s, has been resolved.' % instance.issue_name
		new_notification = Notification.objects.create(
				user_to = instance.user,
				note = message,
				note_time = timezone.now()
			)
		new_notification.save()

@receiver(post_save, sender=Maintenance)
def issue_saved(sender, instance, **kwargs):
	if instance.approval_status:
		user_email = instance.requested_user.email
		subject = 'Status Update'
		from_email = 'sterappdev@gmail.com'
		text_content = 'There has been a change on your maintenance request: %s .' % (instance.request_name)
		#email = EmailMessage(subject, text_content, from_email, [user_email], send(fail_silently)=True,)
		#email.send()
		send_mail(subject, text_content, from_email, [user_email])