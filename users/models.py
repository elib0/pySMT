from django.db import models


class Friendship(models.Model):
    def __unicode__(self):
        return self.follower.username

    follower = models.IntegerField(max_length=11)
    followed = models.IntegerField(max_length=11)
    date = models.DateField('Amigos desde', None, False, True)
