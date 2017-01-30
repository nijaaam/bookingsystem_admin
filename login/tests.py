from django.test import TestCase, Client
from login.models import CustomUser
from django.test import TestCase, Client, RequestFactory, LiveServerTestCase
from selenium.webdriver.common.keys import Keys
import json, time
from bksys.models import *
from django.contrib.sessions.middleware import SessionMiddleware
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from django.conf import settings
from django.contrib.auth.models import User
from selenium.webdriver.support.ui import Select

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
