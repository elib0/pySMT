from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    def __unicode__(self):
    	u = User.objects.get(pk=self.follower)
        return u.username

    follower = models.IntegerField(max_length=11)
    followed = models.IntegerField(max_length=11)
    date = models.DateField('Amigos desde', None, False, True)
