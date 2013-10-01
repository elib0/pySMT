from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    def __unicode__(self):
        return self.followed.username

    follower = models.ForeignKey(User, related_name="follower_set")
    followed = models.ForeignKey(User, related_name="followed_set")
    date = models.DateField('Seguido desde', None, False, True)
