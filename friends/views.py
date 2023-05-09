from django.http import JsonResponse
from friends.models import CustomUser, FriendshipRequest, Friendship
from django.forms.models import model_to_dict
from django.db import IntegrityError

# -----------------GET REQUESTS:-----------------------

def get_users(request):
    response = {}
    status_code = 200
    if request.method == 'GET':
        response['users'] = list(CustomUser.objects.values())
        response['status'] = 0
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)


def get_user(request, **kwargs):
    response = {}
    status_code = 200
    if request.method == 'GET':
        try:
            response['user'] = model_to_dict(CustomUser.objects.get(pk=kwargs['pk']))
        except:
            response['error'] = 'No such user'
            status_code = 404
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)


def get_friendship_requests(request, **kwargs):
    response = {}
    status_code = 200
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(pk=kwargs['pk'])
            response['requests'] = list((FriendshipRequest.objects.filter(sender=user) | FriendshipRequest.objects.filter(reciever=user)).values())
        except Exception as error:
            print(error)
            response['error'] = 'No such user'
            status_code = 404
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)


def get_sent_requests(request, **kwargs):
    response = {}
    status_code = 200
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(pk=kwargs['pk'])
            response['requests'] = list(FriendshipRequest.objects.filter(sender=user).values())
        except Exception as error:
            response['error'] = 'No such user'
            status_code = 404
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)


def get_recieved_requests(request, **kwargs):
    response = {}
    status_code = 200
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(pk=kwargs['pk'])
            response['requests'] = list(FriendshipRequest.objects.filter(reciever=user).values())
        except Exception as error:
            response['error'] = 'No such user'
            status_code = 404
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)


def get_friends(request, **kwargs):
    response = {}
    status_code = 200
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(pk=kwargs['pk'])
            response['users'] = list(user.get_friends().values())
        except Exception as error:
            response['error'] = 'No such user'
            status_code = 404
    else:
        response['error'] = 'Wrong method'
        status_code = 405

    return JsonResponse(response, safe=False, status=status_code)

# -----------------POST REQUESTS:-----------------------

def register_user(request):
    response = {}
    status_code = 200
    if request.method == 'POST':
        response['status'] = 0
        try:
            username = request.POST['username']
            user = CustomUser.objects.create(username=username)
            user.save()
            status_code = 201
            response['message'] = f'User {username} is currently registered'
        except IntegrityError as error:
            response['error'] = 'There is already a user with this username'
            response['status'] = 1
        except Exception as error:
            response['error'] = 'No parameter: username'
            response['status'] = 1
    else:
        response['error'] = 'Wrong method'
        status_code = 405

    return JsonResponse(response, safe=False, status=status_code)


def add_friend(request, **kwargs):
    response = {}
    status_code = 200
    if request.method == 'POST':
        response['status'] = 0
        try:
            reciever = CustomUser.objects.get(pk=request.POST['user_id'])
            sender = CustomUser.objects.get(pk=kwargs['pk'])
            if sender == reciever:
                response['error'] = 'User cant send friendship request to himself'
                response['status'] = 1
            else:
                request_code = sender.add_friend(reciever)
                if request_code == 0:
                    response['message'] = f'{str(sender)} send friendship request to {str(reciever)}'
                else:
                    response['message'] = 'Request was not sent'
                    response['status'] = 1

        except CustomUser.DoesNotExist:
            response['error'] = 'No such user'
            response['status'] = 1
        except Exception as error:
            print(error)
            response['error'] = 'No parameter: user_id'
            response['status'] = 1
    else:
        response['error'] = 'Wrong method'
        status_code = 405

    return JsonResponse(response, safe=False, status=status_code)


def delete_friend(request, **kwargs):
    response = {}
    status_code = 200
    if request.method == 'POST':
        response['status'] = 0
        try:
            user = CustomUser.objects.get(pk=kwargs['pk'])
            friend = CustomUser.objects.get(pk=request.POST['user_id'])

            if Friendship.objects.filter(user1=user, user2=friend).exists():
                Friendship.objects.filter(user1=user, user2=friend).first().delete()
                FriendshipRequest.objects.filter(sender=user, reciever=friend).first().delete()
                response['message'] = f'{str(user)} unfriended {str(friend)}'
            elif Friendship.objects.filter(user1=friend, user2=user).exists():
                Friendship.objects.filter(user1=friend, user2=user).first().delete()
                FriendshipRequest.objects.filter(sender=friend, reciever=user).first().delete()
                response['message'] = f'{str(user)} unfriended {str(friend)}'
            else:
                response['message'] = f'{str(user)} and {str(friend)} are not the friends'
                response['status'] = 1
        except CustomUser.DoesNotExist:
            response['error'] = 'No such user'
            response['status'] = 1
        except Exception as error:
            print(error)
            response['error'] = 'No parameter: user_id'
            response['status'] = 1
    else:
        response['error'] = 'Wrong method'
        status_code = 405

    return JsonResponse(response, safe=False, status=status_code)


def accept_friendship_request(request, **kwargs):
    response = {}
    status_code = 200
    if request.method == 'POST':
        response['status'] = 0
        try:
            user = CustomUser.objects.get(pk=kwargs['pk'])
            friendship_request = FriendshipRequest.objects.get(pk=kwargs['pk_req'])
            if friendship_request.accept(user) == 1:
                response['message'] = f'{str(user)} cant accept {str(friendship_request)}'
                response['status'] = 1
            else:
                response['message'] = f'{str(friendship_request)} has been accepted'.capitalize()
            
        except Exception as error:
            response['error'] = 'No such user'
            response['status'] = 1
            status_code = 404
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)


def reject_friendship_request(request, **kwargs):
    response = {}
    status_code = 200
    if request.method == 'POST':
        response['status'] = 0
        try:
            user = CustomUser.objects.get(pk=kwargs['pk'])
            friendship_request = FriendshipRequest.objects.get(pk=kwargs['pk_req'])
            if friendship_request.reject(user) == 1:
                response['message'] = f'{str(user)} cant reject {str(friendship_request)}'
                response['status'] = 1
            else:
                response['message'] = f'{str(friendship_request)} has been rejected'.capitalize()
            
        except Exception as error:
            response['error'] = 'No such user'
            response['status'] = 1
            status_code = 404
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)


def get_relation_status(request, **kwargs):
    response = {}
    status_code = 200
    if request.method == 'POST':
        response['status'] = 0
        try:
            user = CustomUser.objects.get(pk=kwargs['pk'])
            user_with = CustomUser.objects.get(pk=request.POST['user_id'])

            if user == user_with:
                response['error'] = 'User cant be compared to himself'
                response['status'] = 0
            elif Friendship.objects.filter(user1=user, user2=user_with).exists() or Friendship.objects.filter(user1=user_with, user2=user).exists():
                response['status'] = 'friendship'
                response['message'] = f'{user} and {user_with} are friends'
            elif FriendshipRequest.objects.filter(sender=user, reciever=user_with).exists():
                response['status'] = 'sent'
                response['message'] = f'{user} has sent a friendship request to {user_with}'
            elif FriendshipRequest.objects.filter(sender=user_with, reciever=user).exists():
                response['status'] = 'recieved'
                response['message'] = f'{user} recieved a friendship request from {user_with}'
            else:
                response['status'] = 'None'
                response['message'] = f'{user} and {user_with} are not related to each other'
            
        except Exception as error:
            response['status'] = 1
            response['error'] = 'No such user or users'
            status_code = 404
    else:
        response['error'] = 'Wrong method'
        status_code = 405
    return JsonResponse(response, safe=False, status=status_code)
