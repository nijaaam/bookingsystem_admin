from django.test import TestCase, Client, RequestFactory
from login.models import CustomUser
from bksys.models import rooms
from bksys.views import logout
from bksys.views import *
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
        self.assertRedirects(response,'/')

    def testGetRoom(self):
        rooms.objects.create(room_id=1,room_name="name",room_size="10",room_location="location",room_features="features")
        request = self.factory.post('/getroom/')
        request.POST['name'] = "name"
        response = getroom(request)
        self.assertEqual(response.status_code,200)
        self.assertContains(response,' <input type="text" class="form-control" id="name" name="name" value="name">')
    