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

from transferguideApp.views import render_template

urlpatterns = [
#     # Route, View (Function that returns HTTP Response) -> Returns HTTP Response
#     # path('/', views.index),
#     path('', views.index),
#
    path('search/', render_template),
]