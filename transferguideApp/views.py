from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


