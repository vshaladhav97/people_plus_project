from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "dob"]

class UserGallaryAdmin(admin.ModelAdmin):
    list_display = ["user_id", "caption",]

class UserFollowerAndFollowedAdmin(admin.ModelAdmin):
    list_display = ["user_id",]

admin.site.register(User, UserAdmin)
admin.site.register(UserGallary, UserGallaryAdmin)
admin.site.register(UserFollowerAndFollowed, UserFollowerAndFollowedAdmin)
