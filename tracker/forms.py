from django import forms
from .models import Issue, Maintenance

class IssueForm(forms.ModelForm):

	class Meta:
		model = Issue
		fields = ('issue_name', 'description',)
		widgets = {
			'issue_name': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
			'description': forms.TextInput(attrs={'class': 'mdl-textfield__input'})
		}

class MaintenanceForm(forms.ModelForm):

	class Meta:
		model = Maintenance
		fields = ('request_name', 'description',)