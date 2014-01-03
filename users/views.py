# Create your views here.


from django import forms

from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from rest_framework.authtoken.models import Token

from rest_framework import status, parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view

from rest_framework.response import Response
from rest_framework.views import APIView
from tastypie.authentication import *

from users.models import UserProfile
from school.models import Grade, School


@api_view(['POST'])
def create_auth(request):
    print request.POST
    data = request.POST
    f = forms.EmailField()
    if (not f.clean(data['email'])):
        print(f.clean(data['email']))
        print("neki narobe z mejlom")
        return Response({'messege': 'invalid email'}, status=status.HTTP_400_BAD_REQUEST)
    elif (User.objects.filter(email = data['email']).exists()):
        print ("kao ze obstaja")
        return Response({'messege': 'already exists'}, status = status.HTTP_400_BAD_REQUEST)
    else:
        try:
            school = School.objects.get(id=data['school_id'])
        except Grade.DoesNotExist:
            return Response({'messege': 'school does not exists'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            grade = Grade.objects.get(school = data['school_id'], grade_number = data['grade_number'],
                                            grade_letter = data['grade_letter'])
        except Grade.DoesNotExist:
            grade = Grade.objects.create(
                school = school,
                grade_number = data['grade_number'],
                grade_letter = data['grade_letter']

            )
            grade.save()


        user = User.objects.create_user(
            email=data['email'],
            username=data['email'],
            password=data['password1'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )

        user.save()

        print grade
        print user
        user_profile = UserProfile.objects.create(user=user, grade_participant = grade)
        user_profile.grade_participant = grade
        user_profile.save()

        message_txt = "http://192.168.1.6:8000/user/activate-user/key=" + user_profile.activation_key

        #subject = "%s" % (unicode((u"registration successful")))
        #send_al_email(settings.EMAIL_HOST_USER, [user.email], None, subject, message_txt)
        
        return Response({'messege': 'created'}, status=status.HTTP_201_CREATED)
    #return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
    

def send_al_email(sender, to=None, bcc=None, subject=None, txt=None, html=None, attachment=None):
    message = EmailMultiAlternatives(subject, txt, sender, to, bcc, headers={'Reply-To': sender})
    #message.attach_alternative(html, "text/html")
    message.content_subtype = "html"
    message.send()


def activate_user(request, key):
    current_userProfile = UserProfile.objects.get(activation_key=key)
    print(key)
    current_user = current_userProfile.user
    current_user.is_active=True
    current_user.save()
    current_userProfile.save()
    return HttpResponse("Succesfully registered", content_type="text/plain")
        #return HttpResponse("registration succesfull")


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])

            u = UserProfile.objects.get(user=serializer.object['user'])
            grade = u.grade_participant.id
            return Response({'token': token.key, 'grade_id': grade})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_auth_token = ObtainAuthToken.as_view()
