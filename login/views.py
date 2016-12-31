from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import json
from django.contrib.auth import authenticate, login


def index(request):
	if 'username' in request.POST and 'password' in request.POST:
		return auth(request)
	else:
		return render(request,"home.html",{})

def auth(request):
	user = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=user, password=password)
	if user is not None:
		login(request,user)
		return render(request,"home.html",{})
	else:
		return render(request,"login.html",{'msg':'Wrong Input, Try again.'})
	print user,password
	return HttpResponse(0)
