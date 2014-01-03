from models import *

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET', 'POST'])
def get_schools(request):
    r = []

    schools = School.objects.all()

    for s in schools:
        r.append(school_to_dict(s))

    return JSONResponse(r)


def school_to_dict(school):
    r = {
        "school_id": school.id,
        "school_name": school.name
    }


    return r