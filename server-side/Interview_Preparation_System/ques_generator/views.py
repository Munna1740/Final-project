from django.shortcuts import render
from .models import *
from django.apps import apps

# Create your views here.
def index(request):
    user_info_model = apps.get_model('user','UserInfo')
    skills = user_info_model.objects.get(user=request.user)
    skill1 = skills.key_skills.split()
    questions = Questions.objects.filter(tag__contains=skills.key_skills)
    print(questions)
    return render(request, 'questions.html')
