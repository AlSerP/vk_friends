from django.http import JsonResponse
from friends.models import CustomUser
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError


def get_users(request):
    response = {}
    status_code = 200
    if request.method == 'GET':
        response = list(CustomUser.objects.values())
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)


def get_user(request, pk):
    response = {}
    status_code = 200
    if request.method == 'GET':
        try:
            response = model_to_dict(CustomUser.objects.get(pk=pk))
        except:
            response['error'] = 'No such user'
            status_code = 404
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)


@csrf_exempt
def register_user(request):
    response = {}
    status_code = 200
    if request.method == 'GET':
        response['error'] = 'Wrong method'
        status_code = 405
    if request.method == 'POST':
        try:
            username = request.POST['username']
            user = CustomUser.objects.create(username=username)
            user.save()
            status_code = 201
            response['message'] = f'User {username} is currently registered'
        except IntegrityError as error:
            response['error'] = 'There is already a user with this username'
            status_code = 409
        except Exception as error:
            response['error'] = 'Failed to register: no username parameter'
            status_code = 400

    return JsonResponse(response, safe=False, status=status_code)
