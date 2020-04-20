import json
from django.http import HttpResponse


def re_request(request):
    return json.loads(request.body.decode('utf-8'))


def re_response(data, state=1):
    return HttpResponse(json.dumps(
        {'stat': state,
         'data': data
         }
    ))
