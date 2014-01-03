from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from school import urls as school_urls
from users import urls as user_urls
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'solko.views.home', name='home'),
    # url(r'^solko/', include('solko.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^school/', include(school_urls)),
    url(r'^login/', include(user_urls)),
    url(r'' + '(?P<grade_id>[\d]+)/subjects/', include('subjects.urls', namespace="subjects")),
    url(r'' + '(?P<grade_id>[\d]+)/obligations/', include('obligations.urls', namespace="obligations"))

)
