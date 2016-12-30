from django.shortcuts import render
from django.shortcuts import render_to_response

def index(request):
	return render(request,"home.html",{})
