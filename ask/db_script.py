import os
import sys
sys.path.append('/home/arthur/ask-artur')
os.environ['DJANGO_SETTINGS_MODULE'] = 'askArtur.settings'

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from ask.models import Question, CustomUser, Answer
from ask.forms import AnswerForm, QuestionForm, RegForm, LoginForm
from django.core.urlresolvers import reverse
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def add_user(request):
	for i in range(1502, 2000):
		u = User.objects.create_user(
			username=str(i),
			first_name=(i * 10),
			last_name=str(i * 100),
			email="www@mail.ru",
			password=str(i),
			)
		u.save()
		customuser = CustomUser(user = u, rate = 0)
		customuser.save()