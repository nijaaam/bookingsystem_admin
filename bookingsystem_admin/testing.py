from bookingsystem_admin.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'adminbksysdev',
        'USER': 'root',
        'PASSWORD': '123',
    },
    'rooms': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'bksysdev',
        'USER': 'root',
        'PASSWORD': '123',
    }
}
