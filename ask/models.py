from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomUser(models.Model):
	user = models.OneToOneField(User)
	rate = models.IntegerField(default=0)
    	def __unicode__(self):
        	return self.user.username

class Question(models.Model):
	title = models.CharField(max_length=100)
	question_text = models.CharField(max_length=400)
	customuser = models.ForeignKey(CustomUser)
	pub_data = models.DateTimeField('date published')
	rating = models.IntegerField(default=0, blank=True, null=True)
    	def __unicode__(self):
        	return self.title

class Answer(models.Model): 
	ansver_text = models.CharField(max_length=400)
	customuser = models.ForeignKey(CustomUser)
	question = models.ForeignKey(Question)
	pub_data = models.DateTimeField('date published')
	flag = models.BooleanField(default='false')
	rating = models.IntegerField(default=0, blank=True, null=True)
    	def __unicode__(self):
        	return self.ansver_text