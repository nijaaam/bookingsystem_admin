from django.conf.urls import url
from . import views

urlpatterns = [ url(r'^$',views.index, name = 'index'),
				url(r'^add_room/$',views.add_room, name = 'add_room'),
				url(r'^newroom_template/$',views.newroom_template, name = 'newroom_template'),

				]