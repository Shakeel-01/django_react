from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.db import models


class UserAdminConfig(UserAdmin):
    model = UserAccount
    search_fields = ('email', 'username', 'first_name',)
    list_filter = ('email', 'username', 'first_name',
                   'is_active', 'is_staff', 'created_on')
    ordering = ('-created_on',)
    list_display = ('email', 'username', 'first_name',
                    'is_active', 'is_staff', 'created_on')
    fieldsets = (
        (None, {'fields': ('email', 
         'username', 'first_name', 'last_name',)}),
        ('Picture', {'fields': ('picture',)}),
        ('Role', {'fields': ('role',)}),
        ('Personal', {'fields': ('bio', 'about',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_admin')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )

admin.site.register(UserAccount, UserAdminConfig)

admin.site.register(OnlineStatus)

