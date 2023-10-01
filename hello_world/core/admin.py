# Register your models here.
from django.contrib import admin
from .models import UserProfile, BulletPoint

admin.site.register(UserProfile)
admin.site.register(BulletPoint)
