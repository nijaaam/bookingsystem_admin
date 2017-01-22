from __future__ import unicode_literals
from django.db import models

class rooms(models.Model):
    room_id         = models.AutoField(primary_key=True)
    room_name       = models.CharField(max_length=60, null = False)
    room_size       = models.IntegerField(null = False)
    room_location   = models.TextField(null = False)
    room_features   = models.TextField(null = False)
    in_use          = models.BooleanField(default=True)
    
    def getRoomName(self):
        return self.room_name

    class Meta:
        db_table = "rooms"

    