from django.db import models
from typing import Type


class CustomUser(models.Model):
    """Default User model"""
    username = models.CharField(max_length=32, unique=True, null=False)

    def add_friend(self, user) -> None:
        if not (Friendship.objects.filter(user1=user, user2=self).exists() or Friendship.objects.filter(user1=self, user2=user).exists()):
            request_received = FriendshipRequest.objects.filter(sender=user, reciever=self).first()
            if request_received:
                    friendship = Friendship.objects.create(user1=user, user2=self)
                    friendship.save()
                    request_received.is_confirmed = True
                    request_received.save()
            elif not FriendshipRequest.objects.filter(sender=self, reciever=user).exists():
                friendship_request = FriendshipRequest.objects.create(sender=self, reciever=user)
                friendship_request.save()

    def get_friends(self) -> models.QuerySet:
        friends_id = []
        for friendship in Friendship.objects.filter(user1=self):
            friends_id.append(friendship.user2.pk)
        for friendship in Friendship.objects.filter(user2=self):
            friends_id.append(friendship.user1.pk)

        friends_querset = CustomUser.objects.filter(pk__in=friends_id)

        return friends_querset

    def __str__(self) -> str:
        return self.username


class FriendshipRequest(models.Model):
    """Friendship request between two users"""
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reciever')
    is_confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'request from {str(self.sender)} to {str(self.reciever)}'


class Friendship(models.Model):
    """Friendship between two users"""
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user2')

    def __str__(self) -> str:
        return f'{str(self.user2)} is a friend of {str(self.user1)}'
