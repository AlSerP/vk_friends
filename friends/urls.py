from django.urls import path
from friends.views import *

urlpatterns = [
    path('', get_users, name='users'),
    path('register/', register_user, name='registration'),

    path('<int:pk>/requests/sent', get_sent_requests, name='sended_requests'),
    path('<int:pk>/requests/recieved', get_recieved_requests, name='recieved_requests'),
    path('<int:pk>/requests/<int:pk_req>/accept/', accept_friendship_request, name='accept_requests'),
    path('<int:pk>/requests/<int:pk_req>/reject/', reject_friendship_request, name='reject_requests'),
    path('<int:pk>/requests/', get_friendship_requests, name='requests'),

    path('<int:pk>/friends/add/', add_friend, name='add_friend'),
    path('<int:pk>/friends/delete/', delete_friend, name='delete_friend'),
    path('<int:pk>/friends/', get_friends, name='friends'),

    path('<int:pk>/status_with/', get_relation_status, name='relation_status'),
    path('<int:pk>/', get_user, name='user'),
]
