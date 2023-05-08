from django.http import JsonResponse
import json


def get_api_docs(request):
    f = open('docs/openapi.json')
    data = json.load(f)
    f.close()

    return JsonResponse(data, safe=False, status=200)
