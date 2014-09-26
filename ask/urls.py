from django.conf.urls import patterns, url

from ask import views

urlpatterns = patterns('',
    url(r'^$', views.questions, name='questions'),
    url(r'^popular/$', views.questions_pop, name='questions_pop'),
    url(r'^question/(?P<question_id>\d+)/$', views.detail, name='detail'),
    url(r'^userpage/(?P<user_id>\d+)/$', views.userpage, name='userpage'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^reg/$', views.reg, name='reg'),
    url(r'^question/(?P<question_id>\d+)/newanswer/$', views.newanswer, name='newanswer'),
    url(r'^newquestion/$', views.newquestion, name='newquestion'),
    url(r'^answer/(?P<answer_id>\d+)/like/$', views.answerlike, name='answerlike'),
    url(r'^answer/(?P<answer_id>\d+)/dislike/$', views.answerdislike, name='answerdislike'),
    url(r'^question/(?P<question_id>\d+)/like$', views.questionlike, name='questionlike'),
    url(r'^question/(?P<question_id>\d+)/dislike$', views.questiondislike, name='questiondislike'),
    url(r'^answer/(?P<answer_id>\d+)/goodanswer$', views.goodanswer, name='goodanswer'),
    url(r'^adduser/$', views.add_user, name='add_user'),
    url(r'^addquestion/$', views.add_question, name='add_question'),
    url(r'^addanswer/$', views.add_answer, name='add_answer'),
)