from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from school.views import get_schools
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #
    url(r'^get_school', get_schools, name='home'),

)
