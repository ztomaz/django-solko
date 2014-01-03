from django.db import models

# Create your models here.


# Create your views here.
from django.contrib.auth.models import User
from django.db import models
from school.models import Grade
from django.contrib import admin

CHOICES = [
    'MON',
    'TUE',
    'WED',
    'THU',
    'FRI',
    'SAT',
    'SUN'
]


class TimeStamp(models.Model):
    day = models.CharField(max_length=50)
    tm = models.CharField(max_length=5)


class Subject(models.Model):
    name = models.CharField(max_length=50)
    grade = models.ForeignKey(Grade, null=False)
    participants = models.ManyToManyField(User, blank=True)
    time = models.ManyToManyField(TimeStamp, blank=True)

    def __unicode__(self):
        return self.name

    def save(self):
        super(Subject, self).save()


admin.site.register(Subject)
admin.site.register(TimeStamp)