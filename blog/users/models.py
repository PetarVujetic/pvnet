from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True)

    class Meta:
        verbose_name_plural = 'ProfileUsers'

    def __str__(self):
        return self.user.username

class Follower(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followers')


    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return self.follower.user.username + " follows " +  self.following.user.username
