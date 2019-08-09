from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from .forms import UserChangeForm, UserCreationForm

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('uid', 'profile_image', 'thumbnail_image', 'state_msg','name','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('uid', 'name','password')}),
        ('Personal info', {'fields': ('profile_image','thumbnail_image','state_msg')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('uid', 'name','state_msg','password1', 'password2')}
        ),
    )
    search_fields = ('uid',)
    ordering = ('uid',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)