from django.http import JsonResponse
from friends.models import CustomUser, FriendshipRequest
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


def get_sended_requests(request, pk):
    response = {}
    status_code = 200
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(pk=pk)
            response = list(FriendshipRequest.objects.filter(sender=user).values())
        except Exception as error:
            print(error)
            response['error'] = 'No such user'
            status_code = 404
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)


def get_recieved_requests(request, pk):
    response = {}
    status_code = 200
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(pk=pk)
            response = list(FriendshipRequest.objects.filter(reciever=user).values())
        except Exception as error:
            print(error)
            response['error'] = 'No such user'
            status_code = 404
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)


def get_friends(request, pk):
    response = {}
    status_code = 200
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(pk=pk)
            response = list(user.get_friends().values())
        except Exception as error:
            print(error)
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
            response['error'] = 'No parameter: username'
            status_code = 400

    return JsonResponse(response, safe=False, status=status_code)


@csrf_exempt
def add_friend(request, pk):
    response = {}
    status_code = 200
    if request.method == 'GET':
        response['error'] = 'Wrong method'
        status_code = 405
    if request.method == 'POST':
        try:
            reciever = CustomUser.objects.get(pk=request.POST['user_id'])
            sender = CustomUser.objects.get(pk=pk)
            if sender == reciever:
                response['error'] = 'User cant send friendship request to himself'
                status_code = 400
            else:
                sender.add_friend(reciever)
                response['message'] = f'User {str(sender)} send friendship request to {str(reciever)}'
        except Exception as error:
            print(error)
            response['error'] = 'No parameter: user_id'
            status_code = 400

    return JsonResponse(response, safe=False, status=status_code)
