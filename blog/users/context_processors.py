from django.contrib.auth.models import User

from entries.models import Entry

from .models import Follower, Notification, UserProfile


def extras(request):
  notifications_count = 0
  notification = False
  if request.user.is_authenticated:
    user = request.user
    notifications = Notification.objects.all().filter(notified_user=user)
    notifications_count = notifications.count()
    if notifications_count>0:
      notification = True
    
  return {'notifications_count' : notifications_count, 'notification' : notification}
