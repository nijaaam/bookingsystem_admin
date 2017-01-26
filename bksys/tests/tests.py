from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from login.models import CustomUser
from bksys.models import rooms
from bksys.views import logout
from bksys.views import *
import json, time
from django.contrib.sessions.middleware import SessionMiddleware
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from django.conf import settings
import socket

'''
class viewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        CustomUser.objects.create_superuser('name','123')
        #Run if keepdb is enabled
        roooms.objects.all().delete()

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
        print response
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
'''
class requirementsTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        CustomUser.objects.create_superuser('user','123')
        self.browser.get("http://localhost:8081")

    def insertInput(self,id,value):
        self.browser.find_element_by_id(id).clear()
        self.browser.find_element_by_id(id).send_keys(value)
    
    def insertInputbyName(self,name,value):
        self.browser.find_element_by_name(name).clear()
        self.browser.find_element_by_name(name).send_keys(value)
    
    def tearDown(self):  
        self.browser.quit()
    '''
    def testAddroom(self):
        rooms.objects.all().delete() 
        self.insertInput('username','user')
        self.insertInput('password','123')
        self.browser.implicitly_wait(3)
        self.browser.find_element_by_tag_name('button').click()
        self.browser.implicitly_wait(3)
        self.browser.find_element_by_xpath('//a[contains(text(),"Add Room")]').click()
        self.browser.implicitly_wait(3)
        self.insertInputbyName('name','name_test')
        self.insertInputbyName('size',10)
        self.insertInputbyName('location','loc')
        self.insertInputbyName('features','feat')
        self.browser.find_element_by_xpath('//button[contains(text(),"Add Room")]').click()
        self.browser.implicitly_wait(5)
        time.sleep(3)
        room = rooms.objects.get(room_name='name_test')
        self.assertEqual(room.room_size,10)
        self.assertEqual(room.room_location,'loc')
        self.assertEqual(room.room_features,'feat')
    
    def testViewRoom(self):
        rooms.objects.all().delete() 
        self.insertInput('username','user')
        rooms.objects.create(room_name='new_room',room_size=10,room_location='loc',room_features=   'feat')
        self.insertInput('password','123')
        self.browser.implicitly_wait(3)
        self.browser.find_element_by_tag_name('button').click()
        self.browser.implicitly_wait(3)
        self.insertInput('search','new_room')
        self.browser.find_element_by_id('search_submit').click()
        time.sleep(1)
        self.assertEqual(self.browser.find_element_by_id('name').get_attribute("value"),'new_room')
        #testing Update
        self.insertInput('features','new_feat')
        self.browser.find_element_by_xpath('//button[contains(text(),"Update")]').click()
        time.sleep(2)
        self.assertEqual(rooms.objects.get(room_name='new_room').room_features,"new_feat")
        ##testing block/unblock
        self.browser.find_element_by_id('block').click()
        time.sleep(2) 
        self.assertEqual(rooms.objects.get(room_name='new_room').in_use,False)
        time.sleep(3)
    
    def testFailedLogin(self):
        rooms.objects.all().delete() 
        self.insertInput('username','user')
        self.insertInput('password','1233')
        self.browser.find_element_by_tag_name('button').click()
        self.assertEqual(self.browser.find_element_by_id('msg').text, "Wrong Input, Try again.")
    '''