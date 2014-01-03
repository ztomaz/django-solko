from django.db import models

# Create your models here.


# Create your views here.
from django.contrib.auth.models import User
from django.db import models

from django.contrib import admin


class School(models.Model):

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)


    def __unicode__(self):
        return self.name

    def save(self):
        super(School, self).save()


class Grade(models.Model):
    grade_number = models.IntegerField(max_length=1)
    grade_letter = models.CharField(max_length=1)
    school = models.ForeignKey(School, null=False)
    users = models.ManyToManyField(User, related_name="grade_users", null=True, blank=True)

    def __unicode__(self):
        return str(self.grade_number) + "." + str(self.grade_letter)


admin.site.register(Grade)
admin.site.register(School)