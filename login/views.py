from django.shortcuts import render,render_to_response
from django.http import HttpResponse
import json
from django.contrib.auth import authenticate


def index(request):
	return render(request,"home.html",{})

def auth(request):
	user = request.POST['name']
	password = request.POST['pass']
	user = authenticate(username=user, password=password)
	if user is not None:
		print "Y"
		# A backend authenticated the credentials
	else:
		print "N"
		# No backend authenticated the credentials
	print user,password
	return HttpResponse(0)
