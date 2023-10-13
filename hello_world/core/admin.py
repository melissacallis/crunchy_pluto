# Register your models here.
from django.contrib import admin
from .models import UserProfile, BulletPoint, Education, Experience, Accomplishments

admin.site.register(BulletPoint)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Accomplishments)

class UserProfileAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        for user_profile in queryset:
            # Handle related records deletion here
            # e.g., BulletPoint.objects.filter(user_profile=user_profile).delete()
            user_profile.delete()

# Register the admin class
admin.site.register(UserProfile, UserProfileAdmin)

