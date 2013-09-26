import datetime
from django.db import models
from django.utils import timezone


class Poll(models.Model):
    def __unicode__(self):
        return self.question

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_vote_count(self):
        total = 0
        votes = self.choice_set.all()
        for v in votes:
            total += v.votes
        return total

    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    def __unicode__(self):
        return self.choice_text

    def get_percentage_votes(self, showDecimals=False):
        p = round((float(self.votes)/float(self.poll.get_vote_count()))*100, 2)
        if not showDecimals:
            p = int(p)
        return p

    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
