from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import rooms
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index(request):
	if request.user.is_authenticated():
		return render(request,"dashb.html",{'username':request.user.username})
	else:
		return redirect('/')
		
def log_out(request):
	logout(request)
	return redirect('/')

def getroom(request):
	name = request.POST['name']
	res = rooms.objects.get(room_name=name)
	if res.in_use == True:
		status = "In Use"
	else :
		status = "Blocked"	
	return render(request,"room_details.html",{
		'id':res.room_id,
		'name':res.room_name,
		'size':res.room_size,
		'location':res.room_location,
		'features':res.room_features,
		'status': status,
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

def update(request):
	id = request.POST['id']
	name =  request.POST['name']
	size = request.POST['size']
	loc = request.POST['loc']
	feat = request.POST['feat']
	obj = rooms.objects.get(room_id=id)
	for key in request.POST:
		if request.POST[key] != " ":
			if key == 'name':
				obj.room_name = request.POST[key]
			elif key == 'size':
				obj.room_size = request.POST[key]
			elif key == 'loc':
				obj.room_location = request.POST[key]
			elif key == 'feat':
				obj.room_features = request.POST[key]
	obj.save()

def change_status(request):
	id = request.POST['id']
	obj = rooms.objects.get(room_id=id)
	if obj.in_use == True:
		obj.in_use = False
	else:
		obj.in_use = True
	obj.save()
	return HttpResponse(1)

def newroom_template(request):
	return render(request,"newroom.html",{})

def viewroom_template(request):
	return render(request,"viewroom.html",{})
