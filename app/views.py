# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth

def index(request):
    return render_to_response('index.html', RequestContext(request))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def accounts_login(request):
    auth.login(request, request.user)
    return HttpResponseRedirect('/')

def login_error(request):
    return render_to_response('index.html', RequestContext(request))
