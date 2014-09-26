from ask.models import Question, CustomUser, Answer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegForm(forms.Form):
	username = forms.CharField(max_length=30)
	first_name = forms.CharField(max_length=30)
	last_name =	forms.CharField(max_length=30)
	email = forms.EmailField(required=True)
	password1 = forms.CharField(max_length=30, widget=forms.PasswordInput)

	def clean_username(self):
		data = self.cleaned_data
		try:
			User.objects.get(username = data['username'])
		except User.DoesNotExist:
			return data['username']
		raise forms.ValidationError('This username is already taken.')

class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=30, widget=forms.PasswordInput)

class QuestionForm(forms.Form):
	title = forms.CharField(max_length=80)
	question_text = forms.CharField(widget=forms.Textarea)
	tags = forms.CharField(max_length=40)

class AnswerForm(forms.Form):
	ansver_text = forms.CharField(max_length=400)