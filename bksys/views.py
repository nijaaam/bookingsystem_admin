from django.shortcuts import render
from django.http import HttpResponse
from .models import rooms

def index(request):
	return render(request,"dashb.html",{'username':'user'})

def add_room(request):
	name = request.POST['name']
	size = request.POST['size']
	location = request.POST['location']
	features = request.POST['features']
	new_room = rooms(room_name=name,room_size=size,room_location=location,room_features=features)
	new_room.save()
	return HttpResponse(1)

def block_room(request):
	rooms.objects.get(room_id=id).update(in_use=False)
	return HttpResponse(1)

def newroom_template(request):
	return render(request,"newroom.html",{})