from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    def __unicode__(self):
        return self.follower.username

    follower = models.ForeignKey(User, related_name='followed_set')
    followed = models.ForeignKey(User, related_name='follower_set')
    date = models.DateField('Amigos desde', None, False, True)
