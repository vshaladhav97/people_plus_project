from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import *
# Create your views here.

def UsersListView(request):
    user_list = loader.get_template('user_list.html')
    user_data   = User.objects.all()
    context = {
        'user_data' : user_data
    }
    return HttpResponse(user_list.render(context, request))