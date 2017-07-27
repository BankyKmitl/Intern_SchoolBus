# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.


class MyUserAdmin(UserAdmin):
    model = User

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'Bus_license', 'studentID')}
         ),
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'Bus_license', 'studentID')}),
    )


admin.site.register(School)
admin.site.register(Bus)
admin.site.register(User, MyUserAdmin)
