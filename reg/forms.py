from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from nocaptcha_recaptcha.fields import NoReCaptchaField

class MyRegistrationForm(UserCreationForm):
	captcha = NoReCaptchaField()

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'username', 'email', 'password')
		widgets = {
			'first_name': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
			'last_name': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
			'username': forms.TextInput(attrs={'class': 'mdl-textfield__input'}),
			'email': forms.TextInput(attrs={'class': 'mdl-textfield__input'})
		}

	def save(self, commit=True):
		user = super(MyRegistrationForm, self).save(commit=False)
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		user.username = self.cleaned_data["username"]
		user.email = self.cleaned_data["email"]
		#user.user_level = self.cleaned_data["user_level"]
		if commit:
			user.save()

		return user

	def __init__(self, *args, **kwargs):
	    super(MyRegistrationForm, self).__init__(*args, **kwargs)

	    self.fields['password1'].widget.attrs['class'] = 'mdl-textfield__input'
	    self.fields['password2'].widget.attrs['class'] = 'mdl-textfield__input'

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')