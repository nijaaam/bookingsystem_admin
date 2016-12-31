from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login

def index(request):
	if 'username' in request.POST and 'password' in request.POST:
		return auth(request)
	else:
		return render(request,"login.html",{})

def auth(request):
	user = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=user, password=password)
	if user is not None:
		login(request,user)
		return redirect('dashboard/')
	else:
		return render(request,"login.html",{'msg':'Wrong Input, Try again.'})
