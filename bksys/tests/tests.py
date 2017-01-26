from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from login.models import CustomUser
from bksys.models import rooms
from bksys.views import logout
from bksys.views import *
import json
from django.contrib.sessions.middleware import SessionMiddleware

class viewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        CustomUser.objects.create_superuser('name','123')

    def testIndexRedirect(self):
        response = self.client.get('/dashboard/')
        self.assertRedirects(response, '/')

    def testIndex(self):
        self.client.post('/' ,{'username':'name','password':'123'})
        response = self.client.get('/dashboard/')
        self.assertEqual(response.context['username'],"name")
        self.assertTemplateUsed(response,"dashb.html")

    def testLogout(self):
        self.client.post('/' ,{'username':'name','password':'123'})
        response = self.client.get('/dashboard/log_out')
        self.assertEqual(response.status_code,301)

    def testGetRoom(self):
        rooms.objects.create(room_name="name",room_size="10",room_location="location",room_features="features")
        request = self.factory.post('/getroom/')
        request.POST['name'] = "name"
        response = getroom(request)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,' <input type="text" class="form-control" id="name" name="name" value="name">')
    
    def testAutocompelte(self):
        rooms.objects.create(room_name="rooom",room_size="10",room_location="location",room_features="features")
        rooms.objects.create(room_name="rooom1",room_size="10",room_location="location",room_features="features")
        rooms.objects.create(room_name="name1",room_size="10",room_location="location",room_features="features")
        self.client.post('/' ,{'username':'name','password':'123'})
        request = self.factory.post('/autocomplete')
        request.POST['search'] = 'roo'
        response = autocomplete(request)
        response = json.loads(response.content)
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0],'rooom')
        self.assertEqual(response[1],'rooom1')

    def testAddroom(self):
        request = self.factory.post('/add_room')
        request.POST['name'] = "name2"
        request.POST['size'] = 10
        request.POST['location'] = "loc"
        request.POST['features'] = "feat"
        response = add_room(request)
        self.assertEqual(rooms.objects.get(room_name="name2").room_location,"loc")

    def testUpdate(self):
        room = rooms.objects.create(room_name="rooom3",room_size=10,room_location="location",room_features="features")
        request = self.factory.post('/update')
        request.POST['id'] = room.room_id
        request.POST['name'] = "rooom3"
        request.POST['size'] = 10
        request.POST['loc'] = "loc"
        request.POST['feat'] = "loc"
        response = update(request)
        self.assertEqual(rooms.objects.get(room_id=room.room_id).room_name,"rooom3")

    def testChangestatus(self):
        room = rooms.objects.create(room_name="rooom4",room_size=10,room_location="location",room_features="features")
        request = self.factory.post('/change_status')
        request.POST['id'] = room.room_id
        response = change_status(request)
        self.assertEqual(rooms.objects.get(room_id=room.room_id).in_use,False)

    def testGettemplates(self):
        self.client.post('/' ,{'username':'name','password':'123'})
        response = self.client.get('/dashboard/newroom_template/')
        self.assertTemplateUsed(response,'newroom.html')
        response = self.client.get('/dashboard/viewroom_template/')
        self.assertTemplateUsed(response,'viewroom.html')

class requirementsTest(LiveServerTestCase):
    def setUp(self):  
        self.browser = webdriver.Firefox()
        CustomUser.objects.create_superuser('name','123')
        self.browser.get("http://localhost:8000")

    def insertInput(self,id,value):
        self.browser.find_element_by_id(id).clear()
        self.browser.find_element_by_id(id).send_keys(value)
    
    def tearDown(self):  
        self.browser.quit()

    def testAddroom(self):
        insertInput('username','user')
        insertInput('password','123')
        self.browser.find_element_by_tag_name('button').click()
