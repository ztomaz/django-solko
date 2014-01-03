from django.contrib.auth.models import User
from django.db import models
from school.models import Grade
from django.utils.translation import ugettext_lazy as _
import random
import string


def generate_url(size=15, chars=string.ascii_letters + string.digits):
    random_url = ''.join(random.choice(chars) for x in range(size))
    return random_url


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(_("Activation key"), max_length=15, blank=True, null=True, unique=True, default=generate_url)
    grade_participant = models.ForeignKey(Grade)
