from django.test import TestCase, Client
from login.models import CustomUser

class viewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        CustomUser.objects.create_superuser('name','123')

    def test_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code,200)

    def test_failed_login(self):
        response = self.client.post('/' ,{'username':'user','password':'123'})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context['msg'],"Wrong Input, Try again.")
       
    def test_passed_login(self):
        response = self.client.post('/' ,{'username':'name','password':'123'})
        self.assertRedirects(response, '/dashboard/')