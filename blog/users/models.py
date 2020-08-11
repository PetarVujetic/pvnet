from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from entries.models import Entry


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True)

    class Meta:
        verbose_name_plural = 'ProfileUsers'

    def __str__(self):
        return self.user.username

class Notification(models.Model):
    notified_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user")
    notification_type = models.TextField(blank=False, null=False)
    notification_maker = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    commented_post = models.ForeignKey(Entry, on_delete = models.CASCADE, null = True)
    notification_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_type + " to " + self.notified_user.username

class NotificationHistory(models.Model):
    notified_user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "userHistory")
    notification_type = models.TextField(blank=False, null=False)
    notification_maker = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    commented_post = models.ForeignKey(Entry, on_delete = models.CASCADE, null = True)
    notification_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_type + "to" + self.notified_user.username

class Follower(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followers')


    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return self.follower.user.username + " follows " +  self.following.user.username
