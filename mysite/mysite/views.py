from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm
from django.contrib import sessions

from forum.models import *

def login(request):
    c={}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    first_name = 0;
    
    if user is not None:
        auth.login(request, user)
        request.session['user'] = username
        return HttpResponseRedirect('/index')
    else:
        return HttpResponseRedirect('/accounts/invalid')

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')
        
    args = {}
    args.update(csrf(request))
    
    args['form'] = UserCreationForm()
    
    return render_to_response('register.html', args)

def register_success(request):
    return render_to_response('register_success.html')

def index(request):
    if request.user.is_authenticated():
        latest_topic_list = Topic.objects.order_by('-created')[:10]
        context = {'latest_topic_list': latest_topic_list, 'full_name': request.user.username}
        return render(request, 'index.html', context)
    else:
        latest_topic_list = Topic.objects.order_by('-created')[:10]
        context = {'latest_topic_list': latest_topic_list, 'full_name': 'Guest'}
        return render(request, 'index.html', context)