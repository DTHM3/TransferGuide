"""transferguide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.account.views import LoginView

from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.template.defaulttags import url
from django.urls import path, include

from django.views.generic import TemplateView

# from transferguide.views import index

urlpatterns = [
    path('', TemplateView.as_view(template_name= "transferguideApp/home.html")),
    path("admin/", admin.site.urls),
    path('guide/', include('transferguideApp.urls')),
]



    # path("admin-account-login/",TemplateView.as_view(template_name="admin.html")),

    # # path('', TemplateView.as_view(template_name="index.html")),
    # path('accounts/', include('allauth.urls')),
    # path('logout', LogoutView.as_view()),

    # path('home/', views.say_hello),

    # path('', render_template), # This is the path for search page

