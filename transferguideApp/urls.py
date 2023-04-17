# from django.contrib import admin
# from django.urls import include, path
# from requests import request
#
# from . import views
# from .views import render_template
#
# app_name = 'transferguideApp'
#
from django.views.generic import TemplateView
from django.urls import path, include
from django.views.generic import TemplateView

from transferguideApp import views

from transferguideApp.views import render_template, course_request, login, list_course_requests, course_request_detail, course_equivalency

urlpatterns = [
    path('search/', render_template, name = 'search'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('course-request/', course_request, name='course-request'),
    path('course-equivalency/', course_equivalency, name='course-equivalency'),
    path('course-requests/', list_course_requests, name='list_course_requests'),
    path('course-requests/<int:id>/', course_request_detail, name='course_request_detail'),
]