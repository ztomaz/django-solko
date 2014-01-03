'''
Created on 30. avg. 2013

@author: Tomaz
'''

from django.contrib.auth.models import User
from django.forms import widgets
from rest_framework import permissions, serializers

from school.models import Grade, School
from users.models import UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    #lists = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='list-detail')
    
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')
        
    def restore_object(self,attrs, instance=None):
        if instance:
            instance.username = attrs['username']
            return instance
        

class UserProfileSerializer(serializers.ModelSerializer):
    #lists = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='list-detail')
    #user = serializers.HyperlinkedRelatedField(many=False, read_only=False, view_name='user_info')
    #print user.data
    #print("<--------------->")
    class Meta:
        model = UserProfile
        fields = ('user', 'color')
        depth = 1