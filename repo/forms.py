from django.contrib.auth.forms import AuthenticationForm
from django import forms
from repo.models import UserData

class UserForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['username', 'password', 'email', 'user_level']
        widgets = {
        	'username': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
        	'password': forms.PasswordInput(attrs={'class': 'mdl-textfield__input'})
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['email']