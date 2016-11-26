from django import forms
from .models import Issue, Maintenance, Document

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

class CreateDocumentForm(forms.ModelForm):

	class Meta:
		model = Document
		fields = ['title', 'url', 'document_category']
		widgets = {
	        'title': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
	        'url': forms.URLInput(attrs={'class': 'mdl-textfield__input'})
	    }