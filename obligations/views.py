# Create your views here.
import json
import datetime

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from obligations.models import Obligation, Score
from school.models import Grade
from subjects.models import Subject, TimeStamp
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


def JSON_parse(string_data):
    return json.loads(string_data)


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
def save_or_edit_obligation(request, grade_id, subject_id, obligation_id):

    data = JSON_parse(request.POST.get('data'))

    if 'obligation_name' in data:
        name = data['obligation_name']
    else:
        return JSON_response({'status': "error"})

    if 'score' in data:
        score = data['score']

    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        return JSON_response({'status': "error"})

    if 'date' in data:
        obj = data['date']
        date = datetime.datetime(year=obj[0], month=obj[1],
                            day=obj[2])
    else:
        return JSON_response({'messege': 'wrong date'})

    if int(obligation_id) != -1:
        try:
            obligation = Obligation.objects.get(id=obligation_id)
            obligation.name = name
            obligation.date = date
            obligation.type = data['type']
            obligation.personal = data['personal']
            obligation.is_score_necessary = data['is_score_necessary']
            obligation.subject = subject

        except Obligation.DoesNotExist:
            return JSON_response({'messege': 'school does not exists'})
    else:

        print "<------------ SO FAR SO GOOD ------------------>"
        print subject
        obligation = Obligation(
            name=name,
            type=data['type'],
            date=date,
            created_by=request.user,
            personal=data['personal'],
            subject=subject
        )
        print "so far so good"
        obligation.save()

    if 'score' in data:
        current_score = Score(
            score=score['score'],
            user=request.user,
            obligation=obligation
        )
        current_score.save()
        obligation.scores.add(current_score)
        obligation.save()

    obligation.subject = subject
    obligation.save()
    return JSON_response(obligation_to_dict(obligation, request.user))


def obligation_to_dict(obligation, user):


    r = {
        "obligation_id": obligation.id,
        "date": [obligation.date.year, obligation.date.month, obligation.date.day],
        "obligation_name": obligation.name,
        "type": obligation.type,
        "personal": obligation.personal,
        "subject_id": obligation.subject.id,
        "is_score_necessary": obligation.is_score_necessary
    }

    return r

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def get_obligations(request, grade_id):
    r = []

    try:
        grade = Grade.objects.get(id=grade_id)
    except Grade.DoesNotExist:
        return JSON_response({"status": "error", "message": "something went wrong"})
    if 'data' in request.POST:
        data = JSON_parse(request.POST.get('data'))
        if 'android_date_time' in data:

            obj = data['android_date_time']
            print obj
            date = datetime.datetime(year=obj[0], month=obj[1],
                                day=obj[2], hour=0, minute=0)
        else:
            return JSON_response({'messege': 'wrong date'})
    else:
        date = datetime.datetime.now()


    user = request.user

    obligations = Obligation.objects.filter(subject__grade=grade, date__gte=date, date__lte=date)
    for o in obligations:
        if not o.personal:
            r.append(obligation_to_dict(o, user))
        elif o.personal and o.created_by==request.user:
            r.append(obligation_to_dict(o, user))
    print r
    return JSON_response(r)