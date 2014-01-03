from django.contrib.auth.models import User
from django.db import models
from subjects.models import Subject

from django.contrib import admin


class Obligation(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=10, blank=True)
    created_by = models.ForeignKey(User)

    is_score_necessary = models.BooleanField(default=True)

    personal = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject)
    # if grade is none then obligation is private


class Score(models.Model):
    score = models.IntegerField(max_length=1)
    user = models.ForeignKey(User)
    obligation = models.ForeignKey(Obligation)


admin.site.register(Obligation)
admin.site.register(Score)