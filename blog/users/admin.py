from django.contrib import admin

from .models import Follower, Notification, NotificationHistory, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Follower)
admin.site.register(Notification)
admin.site.register(NotificationHistory)
