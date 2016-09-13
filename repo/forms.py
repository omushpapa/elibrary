from django.contrib.auth.forms import AuthenticationForm
from django import forms
from repo.models import UserData

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = UserData
        fields = ['username', 'password', 'email', 'user_level']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['email']