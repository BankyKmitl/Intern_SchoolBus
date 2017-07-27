from django import forms
from django.contrib.auth.forms import *
from .models import *
from django.contrib import admin


class DriverForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Driver
        widgets = {
            'gender': forms.RadioSelect
        }


class DriverAdmin(admin.ModelAdmin):
    form = DriverForm


class StudentForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Student
        widgets = {
            'gender': forms.RadioSelect
        }


class StudentAdmin(admin.ModelAdmin):
    form = StudentForm

admin.site.register(Driver, DriverAdmin)
admin.site.register(Student, StudentAdmin)
