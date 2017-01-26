from django.conf.urls import url
from . import views

urlpatterns = [ url(r'^$',views.index, name = 'index'),
				url(r'^add_room/$',views.add_room, name = 'add_room'),
				url(r'^update/$',views.update, name = 'update'),
				url(r'^newroom_template/$',views.newroom_template, name = 'newroom_template'),
				url(r'^viewroom_template/$',views.viewroom_template, name = 'viewroom_template'),
				url(r'^autocomplete/$',views.autocomplete, name = 'autocomplete'),
				url(r'^getroom/$',views.getroom, name = 'getroom'),
				url(r'^change_status/$',views.change_status, name = 'change_status'),
				url(r'^log_out/$',views.log_out, name = 'log_out'),
				]