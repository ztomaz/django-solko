from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from obligations.views import save_or_edit_obligation, get_obligations
from school import urls as school_urls
from users import urls as user_urls
admin.autodiscover()

urlpatterns = patterns('',

    # url(r'^get_obligations', get_subjects, name='get_subjects'),
    #url(r'^enroll_me/(?P<subject_id>-?\d+)$', enroll_me, name='enorll_me'),
    url(r'^save_obligation/(?P<subject_id>-?\d+)/(?P<obligation_id>-?\d+)$', save_or_edit_obligation, name='save_obligation'),
    url(r'^get_obligations', get_obligations, name='get_subjects'),

)
