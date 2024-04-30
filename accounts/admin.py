from django.contrib import admin
from .models import MyUser as User
from .models import Contact
# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display=['id','username','email']

# from .models import MyUser


@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'last_login',
        'is_superuser',
        'username',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'image_profile',
        'cover_profile',
        
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
    )
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=['user_from','user_to','created']
