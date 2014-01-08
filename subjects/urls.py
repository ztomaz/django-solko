from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from subjects.views import get_subjects, enroll_me, save_or_edit_subject, get_statistics

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #
    url(r'^get_subjects', get_subjects, name='get_subjects'),
    url(r'^enroll_me/(?P<subject_id>-?\d+)$', enroll_me, name='enorll_me'),
    url(r'^save_subject/(?P<subject_id>-?\d+)$', save_or_edit_subject, name='save_subject'),
    url(r'^get_statistics', get_statistics, name='get_statistics')
)
