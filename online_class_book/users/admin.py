from django.contrib import admin
from .models import *
# Register your models here.

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class CustomUserAdmin(BaseUserAdmin):
 

    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('first_name','last_name','email','subject','password','age','phone','role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('first_name','email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(CustomUser, CustomUserAdmin)

# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('email','password')


@admin.register(AvailableTime)
class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('id','teacher','start_time','end_time')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id','student','available_time','reserved_starttime','reserved_endtime')


# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('email','password')