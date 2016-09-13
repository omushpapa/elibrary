from django import forms
from .models import Issue, Maintenance

class IssueForm(forms.ModelForm):

	class Meta:
		model = Issue
		fields = ('issue_name', 'description',)

class MaintenanceForm(forms.ModelForm):

	class Meta:
		model = Maintenance
		fields = ('request_name', 'description',)