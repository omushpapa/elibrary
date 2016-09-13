from django.contrib import admin
from django.utils import timezone
from tracker.models import *
from django.core.mail import EmailMessage

class IssueAdmin(admin.ModelAdmin):
	list_display = ('issue_name', 'time_raised', 'is_seen')
	fields = (
			'user',
			'issue_name', 
			'description',
			'handler',
			'priority',
			'status',
			'comments',
			'is_seen',
		)
	readonly_fields = ('user', 'issue_name', 'description',)

class NotificationAdmin(admin.ModelAdmin):
	list_display = ('user_to', 'note', 'note_time')
	fields = ('user_to', 'note', 'note_time',)
	readonly_fields = ('user_to', 'note', 'note_time',)

class MaintenanceAdmin(admin.ModelAdmin):
	list_display = ('request_name', 'time_requested','is_seen', 'progress')
	fields = ('request_name', 'requested_user', 'description',
		'time_requested', 'maintainer','approval_status', 'progress', 'time_resolved', 'comments')
	readonly_fields = ('request_name', 'requested_user', 'description', 'time_requested',)

	def save_model(self, request, obj, form, change):
		admin.ModelAdmin.save_model(self, request, obj, form, change)

		if change:
			obj.is_seen = True
			obj.save()
		if obj.approval_status == 'rejected':
			obj.progress = 'resolved'
			obj.time_resolved = timezone.now
			obj.save()

class MaintainerAdmin(admin.ModelAdmin):
	list_display = ('user', 'contact')

class DocumentAdmin(admin.ModelAdmin):
	list_display = ('title', 'document_category',)

admin.site.register(Issue, IssueAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(Maintainer, MaintainerAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentCategory)
