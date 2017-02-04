from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
import requests, socket
from django.db import connection
import paramiko, subprocess, os

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
	    uwsgi.start()
            r = requests.head('http://localhost')
            if r != 200:
                os.system('uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data')
        except:
            os.system('uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data')
      



