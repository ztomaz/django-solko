# Create your views here.
from _ast import Is
import json
from numpy.distutils.command.scons import scons
from django.contrib.auth.tests.models import IsActiveTestCase

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from obligations.models import Score
from obligations.views import score_to_dict
from school.models import Grade
from subjects.models import Subject, TimeStamp
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class JSON_response(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSON_response, self).__init__(content, **kwargs)

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def get_subjects(request, grade_id):
    r = []
    try:
        grade = Grade.objects.get(id=grade_id)
    except Grade.DoesNotExist:
        return JSON_response({"status": "error", "message": "something went wrong"})

    user = request.user

    subjects = Subject.objects.filter(grade=grade)
    for s in subjects:
        r.append(subject_to_dict(s, user))

    return JSON_response(r)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def enroll_me(request, grade_id, subject_id):
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        return JSON_response({"status": "error", "message": "you stupid man"})

    user = request.user

    subject.participants.add(user)

    return JSON_response({"status": "OK", "message": "you did it"})


def JSON_parse(string_data):
    return json.loads(string_data)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def save_or_edit_subject(request, grade_id, subject_id):

    data = JSON_parse(request.POST.get('data'))

    print data

    if 'subject_name' in data:
        name = data['subject_name']
    else:
        return JSON_response({'status': "error"})
    if 'times' in data:
        times = data['times']

    try:
        grade = Grade.objects.get(id=grade_id)
    except Grade.DoesNotExist:
        return JSON_response({'status': "error"})

    print subject_id

    if int(subject_id) != -1:
        try:
            subject = Subject.objects.get(id=subject_id)
            subject.name=name
        except Subject.DoesNotExist:
            return JSON_response({'messege': 'school does not exists'})
    else:
        subject = Subject(
            name=name,
            grade=grade,
        )
        print "so far so good"
        subject.save()

    subject.time.clear()
    for d in times:
        if int(d['time_id'] == -1):
            t = TimeStamp(
                day=d['time_day'],
                tm=d['time_tm']
            )
            t.save()
        else:
            try:
                t = TimeStamp.objects.get(id=int(d['time_id']))
            except TimeStamp.DoesNotExist:
                return JSON_response({'messege': 'this should not happen'})


        subject.time.add(t)

    subject.save()
    print (subject_to_dict(subject, request.user))
    return JSON_response(subject_to_dict(subject, request.user))

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def get_statistics(request, grade_id):
    r = []
    try:
        grade = Grade.objects.get(id=grade_id)
    except Grade.DoesNotExist:
        return JSON_response({"status": "error", "message": "something went wrong"})

    user = request.user

    subjects = Subject.objects.filter(grade=grade)
    for s in subjects:
        r.append(subject_to_dict_statistics(s, user))

    return JSON_response(r)


def subject_to_dict(subject, user):
    print subject.participants.all()
    if subject.participants.all().filter(id=user.id).exists():
        enrolled = True
    else:
        enrolled = False


    times = []

    for t in subject.time.all():
        times.append(time_to_dict(t))

    r = {
        "subject_id": subject.id,
        "subject_name": subject.name,
        "enrolled":enrolled,
        "times": times
    }

    return r


def subject_to_dict_statistics(subject, user):
    if subject.participants.all().filter(id=user.id).exists():
        enrolled = True
    else:
        enrolled = False

    personal_scores = []
    all_scores = []
    for t in Score.objects.filter(obligation__subject=subject, score__gte=1):
        all_scores.append(score_to_dict(t))
        if (t.user == user):
            personal_scores.append(score_to_dict(t))

    r = {
        "subject_id": subject.id,
        "subject_name": subject.name,
        "enrolled":enrolled,
        "personal_scores": personal_scores,
        "all_scores": all_scores
    }

    return r


def time_to_dict(time):
    r = {
        "time_id": time.id,
        "time_day": time.day,
        "time_tm": time.tm
    }
    return r