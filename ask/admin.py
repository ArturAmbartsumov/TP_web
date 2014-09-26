from django.contrib import admin
from ask.models import CustomUser
from ask.models import Question
from ask.models import Answer

admin.site.register(CustomUser)
admin.site.register(Question)
admin.site.register(Answer)