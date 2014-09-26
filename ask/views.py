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


def questions(request):
	question_list_all = Question.objects.order_by('-pub_data')
	lastreg_list = User.objects.order_by('-date_joined')[:10]
	date_sort=1
	
	paginator = Paginator(question_list_all, 5)
	page = request.GET.get('page')
	try:
		question_list = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		question_list = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		question_list = paginator.page(paginator.num_pages)

	question_form = QuestionForm()
	reg_form = RegForm()
	login_form = LoginForm()

	message = 0
	flag = 0
	if "message" in request.session and "flag" in request.session:
		message = request.session["message"]
		flag = request.session["flag"]
		del request.session["message"]
		del request.session["flag"]

	context = {
		'question_list': question_list,
		'lastreg_list': lastreg_list,
		'question_form': question_form,
		'login_form': login_form,
		'reg_form': reg_form,
		'date_sort': date_sort,
		'message': message,
		'flag': flag,
	}
	return render(request, 'ask/questions.html', context)

def questions_pop(request):
	question_list_all = Question.objects.order_by('-rating', '-pub_data')
	lastreg_list = User.objects.order_by('-date_joined')[:10]
	pop_sort = 1

	paginator = Paginator(question_list_all, 5)
	page = request.GET.get('page')
	try:
		question_list = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		question_list = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		question_list = paginator.page(paginator.num_pages)

	question_form = QuestionForm()
	reg_form = RegForm()
	login_form = LoginForm()

	message = 0
	flag = 0
	if "message" in request.session and "flag" in request.session:
		message = request.session["message"]
		flag = request.session["flag"]
		del request.session["message"]
		del request.session["flag"]

	context = {
		'question_list': question_list,
		'question_form': question_form,
		'lastreg_list': lastreg_list,
		'login_form': login_form,
		'reg_form': reg_form,
		'pop_sort': pop_sort,
		'message': message,
		'flag': flag,
	}
	return render(request, 'ask/questions.html', context)

def detail(request, question_id):
	q = get_object_or_404(Question, pk=question_id)
	answer_list_all = q.answer_set.order_by('-rating', '-pub_data')
	best_answer = q.answer_set.all().filter(flag='true').order_by('-pub_data')

	paginator = Paginator(answer_list_all, 5)
	page = request.GET.get('page')
	try:
		answer_list = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		answer_list = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		answer_list = paginator.page(paginator.num_pages)

	answer_form = AnswerForm()

	message = 0
	flag = 0
	if "message" in request.session and "flag" in request.session:
		message = request.session["message"]
		flag = request.session["flag"]
		del request.session["message"]
		del request.session["flag"]

	context = {
		'question': q,
		'answer_list': answer_list,
		'best_answer': best_answer,
		'answer_form': answer_form,
		'message': message,
		'flag': flag,
	}
	return render(request, 'ask/detail.html', context)

def userpage(request, user_id):
	customuser = get_object_or_404(CustomUser, pk=user_id)
	question_list = customuser.question_set.order_by('-pub_data')[:20]
	answer_list = customuser.answer_set.order_by('-pub_data')[:20]

	message = 0
	flag = 0
	if "message" in request.session and "flag" in request.session:
		message = request.session["message"]
		flag = request.session["flag"]
		del request.session["message"]
		del request.session["flag"]

	context = {
		'customuser': customuser,
		'question_list': question_list,
		'answer_list': answer_list,
		'message': message,
		'flag': flag,
	}
	return render(request, 'ask/userpage.html', context)


def newanswer(request, question_id):
	if request.user.is_authenticated():
		q = get_object_or_404(Question, pk=question_id)
		u = request.user
		user = u.customuser
		answer_form = AnswerForm(request.POST) # A form bound to the POST data
		if answer_form.is_valid(): # All validation rules pass
			answer = Answer(
				ansver_text=answer_form.cleaned_data['ansver_text'],
				customuser=user,
				question=q,
				pub_data=timezone.now(),
				flag=0)
			answer.save()
			request.session["message"] = "Your question was successfully added!!"
			request.session["flag"] = 1
		else:
			request.session["message"] = "Error!!"
			request.session["flag"] = 1
	else:
		request.session["message"] = "You must be logged in"
		request.session["flag"] = 0
	return HttpResponseRedirect(reverse('detail', args=(question_id,))) # Redirect after POST


def newquestion(request):
	if request.user.is_authenticated():
		u = request.user
		user = u.customuser
		question_form = QuestionForm(request.POST) # A form bound to the POST data
		if question_form.is_valid(): # All validation rules pass
			question = Question(
				title=question_form.cleaned_data['title'],
				question_text=question_form.cleaned_data['question_text'],
				customuser=user,
				pub_data=timezone.now()
			)
			question.save()
			request.session["message"] = "Your answer was successfully added!!"
			request.session["flag"] = 1
		else:
			request.session["message"] = "Error!!"
			request.session["flag"] = 1
	else:
		request.session["message"] = "You must be logged in"
		request.session["flag"] = 0
	return HttpResponseRedirect(reverse('questions')) # Redirect after POST

def reg(request):
	reg_form = RegForm(request.POST)
	if reg_form.is_valid():
		user = User.objects.create_user(
			username=reg_form.cleaned_data['username'],
			first_name=reg_form.cleaned_data['first_name'],
			last_name=reg_form.cleaned_data['last_name'],
			email=reg_form.cleaned_data['email'],
			password=reg_form.cleaned_data['password1'],
			)
		user.save()
		customuser = CustomUser(user = user, rate = 0)
		customuser.save()
		request.session["message"] = "Congratulations!! You have successfully registered!!"
		request.session["flag"] = 1
	else:
		request.session["message"] = "Registration error!!"
		request.session["flag"] = 0
	return HttpResponseRedirect(reverse('questions'))

def login(request):
	if not request.user.is_authenticated():
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				auth.login(request, user)
				request.session["message"] = "Successful authorization!!"
				request.session["flag"] = 1
			else:
				request.session["message"] = "Wrong login or password!!"
				request.session["flag"] = 0
	else:
		request.session["message"] = "You are already login!!"
		request.session["flag"] = 0
	return HttpResponseRedirect(reverse('questions'))

def logout(request):
	if request.user.is_authenticated():
		auth.logout(request)
		request.session["message"] = "Successful logout!!"
		request.session["flag"] = 1
	else:
		request.session["message"] = "You must be logged in"
		request.session["flag"] = 0
	return HttpResponseRedirect(reverse('questions'))

def answerlike(request, answer_id):
	answer = get_object_or_404(Answer, pk=answer_id)
	if request.user.is_authenticated():
		answer.rating +=1
		answer.save()
	else:
		request.session["message"] = "You must be logged in"
		request.session["flag"] = 0
	return HttpResponseRedirect(reverse('detail', args=(answer.question.id,)))	

def answerdislike(request, answer_id):
	answer = get_object_or_404(Answer, pk=answer_id)
	if request.user.is_authenticated():
		answer.rating -=1
		answer.save()
	else:
		request.session["message"] = "You must be logged in"
		request.session["flag"] = 0
	return HttpResponseRedirect(reverse('detail', args=(answer.question.id,)))

def questionlike(request, question_id):
	if request.user.is_authenticated():
		question = get_object_or_404(Question, pk=question_id)
		question.rating += 1
		question.save()
	else:
		request.session["message"] = "You must be logged in"
		request.session["flag"] = 0
	return HttpResponseRedirect(reverse('detail', args=(question_id,)))

def questiondislike(request, question_id):
	if request.user.is_authenticated():
		question = get_object_or_404(Question, pk=question_id)
		question.rating -= 1
		question.save()
	else:
		request.session["message"] = "You must be logged in"
		request.session["flag"] = 0
	return HttpResponseRedirect(reverse('detail', args=(question_id,)))

def goodanswer(request, answer_id):
	if request.user.is_authenticated():
		answer = get_object_or_404(Answer, pk=answer_id)
		if request.user.customuser.id == answer.question.customuser.id:
			answer.flag = True
			answer.save()
		else:
			request.session["message"] = "This is not your question!!"
			request.session["flag"] = 0
	else:
		request.session["message"] = "You must be logged in"
		request.session["flag"] = 0
	return HttpResponseRedirect(reverse('detail', args=(answer.question.id,)))

def add_user(request):
	for i in range(6800, 11500):
		u = User.objects.create_user(
			username=str(i*2 + 1),
			first_name=(i * 10),
			last_name=str(i * 100),
			email="www@mail.ru",
			password=str(i),
			)
		u.save()
		customuser = CustomUser(user = u, rate = 0)
		customuser.save()
	return HttpResponseRedirect(reverse('questions'))

def add_question(request):
	u = get_object_or_404(User, pk=12)
	for i in range(5000, 10000):
		question = Question(
			title=int(i),
			question_text="Question",
			customuser=u.customuser,
			pub_data=timezone.now()
			)
		question.save()
	return HttpResponseRedirect(reverse('questions'))

def add_answer(request):
	q = get_object_or_404(Question, pk=2)
	u = get_object_or_404(User, pk=12)
	for i in range(5000, 10000):
		answer = Answer(
			ansver_text=int(i),
			customuser=u.customuser,
			question=q,
			pub_data=timezone.now(),
			flag=0)
		answer.save()
	return HttpResponseRedirect(reverse('questions'))