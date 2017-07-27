# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime


# Create your views here.
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'school_bus/login.html')


@login_required
def logout(request):
    logout_text = "You are logged out. Thanks for Using."
    logout(request)
    return render(request, 'registration/login.html', {'logout_text': logout_text})


@login_required
def home(request):
    filter_data = []
    time = datetime.datetime.now()
    scan_data = Scan_Data.objects.all()
    std_list = []
    student = Student.objects.get(studentID=request.user.studentID_id)
    bus = Bus.objects.get(id=request.user.Bus_license_id)
    for data in scan_data:
        compare = time - data.time
        if compare.total_seconds() <= 60:
            filter_data.append(data)

    for fdata in filter_data:
        try:
            std = Student.objects.get(itag_mac=fdata.itag_mac)
            std_list.append(std)
        except Student.DoesNotExist:
            pass
    return render(request, 'school_bus/home.html',
                  {'scan_data': filter_data, 'std_list': std_list, 'bus': bus, 'student': student})


@login_required
def student_info(request, student_id):
    student = Student.objects.get(studentID__exact=student_id)
    scan_log = Scan_Data.objects.filter(itag_mac__exact=student.itag_mac)
    first_scan = Scan_Data.objects.filter(
        itag_mac__exact=student.itag_mac).last()
    bus = Bus.objects.get(id=request.user.Bus_license_id)
    return render(request, 'school_bus/student_info.html',
                  {'first_scan': first_scan, 'student': student, 'scan_log': scan_log, 'bus': bus, 'student': student})


@login_required
def bus_info(request, bus_license_id):
    student = Student.objects.get(studentID=request.user.studentID_id)
    bus = Bus.objects.get(id__exact=bus_license_id)
    driver = Driver.objects.get(Bus_license_id=bus_license_id)
    return render(request, 'school_bus/bus_info.html', {'bus': bus, 'driver': driver, 'student': student})
