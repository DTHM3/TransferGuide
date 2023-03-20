from django.contrib import admin
from django.urls import include, path
from . import views

app_name = 'transferguideApp'

urlpatterns = [
    # Route, View (Function that returns HTTP Response) -> Returns HTTP Response
    path('home/', views.say_hello),
]