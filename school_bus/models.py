# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

GENDER_CHOICES = ((True, 'Male'), (False, 'Female'))


class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    tel = models.CharField(max_length=15)
    website = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Bus(models.Model):
    license_number = models.CharField(max_length=10)
    license_province = models.CharField(max_length=20)
    number = models.CharField(max_length=3)
    color = models.CharField(max_length=10)
    brand = models.CharField(max_length=20)
    route = models.CharField(max_length=50)
    rpi_mac = models.CharField(max_length=20)
    imei_tracking = models.CharField(max_length=20)
    img = models.ImageField(max_length=100, upload_to='images/bus/')
    school_name = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Buses"
        unique_together = ('license_number', 'license_province')

    def __unicode__(self):
        return self.license_number + ' ' + self.license_province


class Driver(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    gender = models.BooleanField(choices=GENDER_CHOICES, default=True)
    tel = models.CharField(max_length=10)
    img = models.ImageField(max_length=100, upload_to='images/driver/')
    Bus_license = models.ForeignKey(
        Bus, related_name='driver_bus_license', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.firstname + ' ' + self.lastname


class Student(models.Model):
    studentID = models.CharField(max_length=20, primary_key=True, unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    gender = models.BooleanField(choices=GENDER_CHOICES, default=True)
    age = models.IntegerField()
    img = models.ImageField(max_length=100, upload_to='images/student/',
                            blank=True, null=True, default='/images/human.png')
    grade = models.CharField(max_length=100)
    take_address = models.CharField(max_length=100)
    drop_address = models.CharField(max_length=100)
    itag_mac = models.CharField(max_length=20)
    Bus_license = models.ForeignKey(
        Bus, related_name='student_bus_license', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.studentID + ' ' + self.firstname + ' ' + self.lastname


class User(AbstractUser):
    Bus_license = models.ForeignKey(
        Bus, related_name='user_bus_license', on_delete=models.CASCADE, blank=True, null=True)
    studentID = models.ForeignKey(
        Student, on_delete=models.CASCADE, blank=True, null=True)

    def __unicode__(self):
        return self.username


class Scan_Data(models.Model):
    rpi_mac = models.CharField(max_length=20)
    itag_mac = models.CharField(max_length=20)
    time = models.DateTimeField()
    rssi = models.IntegerField()

    class Meta:
        ordering = ['-time']
