from django.urls import path
from friends.views import *

urlpatterns = [
    path('', get_users, name='users'),
    path('register/', register_user, name='registration'),
    path('<int:pk>/', get_user, name='user'),
]
