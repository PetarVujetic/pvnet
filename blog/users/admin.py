from django.contrib import admin
from .models import UserProfile, Follower
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Follower)
