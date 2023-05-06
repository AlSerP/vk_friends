from django.urls import path
from friends.views import *

urlpatterns = [
    path('', get_users, name='users'),
    path('register/', register_user, name='registration'),
    path('<int:pk>/requests/sended', get_sended_requests, name='sended_requests'),
    path('<int:pk>/requests/recieved', get_recieved_requests, name='recieved_requests'),
    path('<int:pk>/friends', get_friends, name='friends'),
    path('<int:pk>/add_friend/', add_friend, name='add_friend'),
    path('<int:pk>/', get_user, name='user'),
]
