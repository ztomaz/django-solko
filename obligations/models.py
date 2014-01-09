from django.contrib.auth.models import User
from django.db import models
from subjects.models import Subject

from django.contrib import admin


class Obligation(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, blank=True)
    created_by = models.ForeignKey(User)
    description = models.CharField(max_length=250, blank=True)
    is_score_necessary = models.BooleanField(default=True)

    personal = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject)
    # if grade is none then obligation is private


class Score(models.Model):
    score = models.IntegerField(max_length=2, blank=True)
    user = models.ForeignKey(User)
    # 0 for completed
    # 1 for failed
    # -1 for pending
    completed = models.IntegerField(default=-1)
    obligation = models.ForeignKey(Obligation)

    def save(self, *args, **kwargs):
        super(Score, self).save()

    class Meta:
        unique_together = ('user', 'obligation',)

admin.site.register(Obligation)
admin.site.register(Score)