from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.views import generic
from django.views.generic import CreateView

from transferguideApp.models import UVAClass
import requests

import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import CourseRequestForm
from transferguideApp.models import UVAClass, News


# Create your views here.
#
# from django.http import HttpResponse
#
# # Function to call an API and return the response as a JSON object
def call_api(request):
    response = requests.get(
        'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01')
    json_response = response.json()
    return JsonResponse(json_response)


# # Function to render a template with the API response data
def render_template(request):
    response = None
    classes = []

    if request.method == 'POST':
        # Define the URL and payload for the POST request
        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1232&page=1'
        response = requests.get(url)
        response = response.json()
        print(response)

        for item in response:
            # data = json.loads(item)

            myclass = UVAClass()
            myclass.class_id = item['crse_id'] + '-' + str(item['crse_offer_nbr'])
            myclass.subject = item['subject']
            myclass.class_description = item['descr']
            myclass.instructors = item['instructors']
            myclass.units = item['units']
            classes.append(myclass)

    return render(request, 'transferguideApp/search.html', {'classes': classes})


def course_request(request):
    if request.method == 'POST':
        form = CourseRequestForm(request.POST)
        if form.is_valid():
            form.save()
            # user = request.user to add after we add authentication
            # User submits response now redirect them to home page
            return redirect('news') #To change after
        else:
            return render(request, 'courserequest/courseRequest.html', {'form': form})
    else:
        form = CourseRequestForm()
        return render(request, 'courserequest/courseRequest.html', {'form': form})


class NewsView(generic.ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'transferguideApp/news.html'

    def get_queryset(self):
        # returns the latest news
        return News.objects.all()
