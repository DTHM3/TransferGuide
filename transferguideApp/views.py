from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


# @login_required
def index():
    return ("Hello, world. You're at the home page")


def say_hello(request):
    return render(request, 'home.html', {})
