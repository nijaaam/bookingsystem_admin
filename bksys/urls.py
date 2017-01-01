from django.conf.urls import url
from . import views

urlpatterns = [ url(r'^$',views.index, name = 'index'),
				url(r'^add_room/$',views.add_room, name = 'add_room'),
				url(r'^newroom_template/$',views.newroom_template, name = 'newroom_template'),
				url(r'^editroom_template/$',views.editroom_template, name = 'editroom_template'),
				url(r'^blockroom_template/$',views.blockroom_template, name = 'blockroom_template'),
				url(r'^autocomplete/$',views.autocomplete, name = 'autocomplete'),
				url(r'^getroom/$',views.getroom, name = 'getroom'),
				url(r'^block_room/$',views.block_room, name = 'block_room'),
				url(r'^unblock_room/$',views.unblock_room, name = 'unblock_room'),
				]