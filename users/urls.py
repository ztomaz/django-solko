from django.conf import settings
from django.conf.urls import include, patterns, url

from users import views

from rest_framework.authtoken import views as authtoken_views

urlpatterns = patterns('',
    #register new user
    url(r'^register', views.create_auth, name='register_user'),
    url(r'^activate-user/key=(?P<key>[\w]+)$', views.activate_user),
    url(r'api-token-auth/?$', views.obtain_auth_token),

)
