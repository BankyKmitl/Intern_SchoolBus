from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^student/(?P<student_id>\w+)', views.student_info, name='student'),
    url(r'^bus/(\d+)', views.bus_info, name='bus'),
]
