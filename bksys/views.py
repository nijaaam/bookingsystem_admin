from django.shortcuts import render
from django.http import HttpResponse
from .models import rooms
import json
from django.contrib.auth.decorators import login_required


def index(request):
	if request.user.is_authenticated():
		print "Y"
	return render(request,"dashb.html",{'username':'user'})

def getroom(request):
	name = request.POST['name']
	res = rooms.objects.get(room_name=name)	
	return render(request,"viewroom.html",{
		'id':res.room_id,
		'name':res.room_name,
		'size':res.room_size,
		'location':res.room_location,
		'features':res.room_features,
	})

def autocomplete(request):
	query = request.POST['search']
	rooms_list = rooms.objects.filter(room_name__contains=query)
	results = [rm_instance.getRoomName() for rm_instance in rooms_list]
	return HttpResponse(json.dumps(results), content_type="application/json")

def add_room(request):
	name = request.POST['name']
	size = request.POST['size']
	location = request.POST['location']
	features = request.POST['features']
	new_room = rooms(room_name=name,room_size=size,room_location=location,room_features=features)
	new_room.save()
	return HttpResponse(1)

def edit_room(request):
	rooms_list = rooms.objects.filter(room_id=room.room_id,date__range=[start,end]) 
	results = [rm_instance.getJSON() for rm_instance in rooms_list]
	return HttpResponse(json.dumps(results), content_type="application/json")

def block_room(request):
	id = request.POST['id']
	print id
	obj = rooms.objects.get(room_id=id)
	obj.in_use = False
	obj.save()
	return HttpResponse(1)

def unblock_room(request):
	id = request.POST['id']
	obj = rooms.objects.get(room_id=id)
	obj.in_use = True
	obj.save()
	return HttpResponse(1)

def newroom_template(request):
	return render(request,"newroom.html",{})

def editroom_template(request):
	return render(request,"editroom.html",{})

def blockroom_template(request):
	return render(request,"blockroom.html",{})