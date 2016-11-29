from django import forms
from .models import Card, TodoList, TodoItem

class CardForm(forms.ModelForm):
	
	class Meta:
		model = Card
		fields = ('card_name', 'description',)
		widgets = {
			'card_name': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
			'description': forms.Textarea(attrs={'class': 'mdl-textfield__input'})
		}

class TodoListForm(forms.ModelForm):

	class Meta:
		model = TodoList
		fields = ('todo_name', 'publicity_status',)
		widgets = {
			'todo_name': forms.TextInput(attrs={'class': 'mdl-textfield__input'})
		}

class MoveCardForm(forms.ModelForm):
	
	todo_name = forms.ModelChoiceField(queryset=TodoList.objects.none())

	class Meta:
		model = TodoList
		fields = ('todo_name',)

	def __init__(self, user, *args, **kwargs):
		super(MoveCardForm, self).__init__(*args, **kwargs)
		self.fields['todo_name'].queryset = TodoList.objects.filter(user=user)	