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
    if not request.user.is_authenticated:
        return redirect('login')
    response = None
    classes = []

    if request.method == 'POST':
        search_type = request.POST['searchType']
        search_value = request.POST['search']
        # print(search_type)
        # print(search_value)

        # Modify the URL and payload based on search_type and search_value
        # For example, if search_type is "subject", you might add a query parameter for the subject
        # You need to update the URL according to the API documentation for the expected search parameters
        url = ""
        subjectURL = f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&subject={search_value.upper()}&page=1"
        instructorURL = f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&page=1&instructor_name={search_value}"
        if (search_type == "subject"):
            url = subjectURL
        elif (search_type == "professor"):
            url = instructorURL
        print(url)
        response = requests.get(url)
        response = response.json()
        print(response)

        for item in response:
            myclass = UVAClass()
            myclass.class_id = item['crse_id'] + '-' + str(item['crse_offer_nbr'])
            myclass.subject = item['subject']
            myclass.class_description = item['descr']
            myclass.instructors = item['instructors']
            myclass.units = item['units']
            classes.append(myclass)

    return render(request, 'transferguideApp/search.html', {'classes': classes})


def course_request(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = CourseRequestForm(request.POST)
        if form.is_valid():
            course_request = form.save(commit=False)
            course_request.user = request.user
            course_request.save()
            # user = request.user to add after we add authentication
            # User submits response now redirect them to home page
            return redirect('home')  # To change after
        else:
            return render(request, 'courserequest/courseRequest.html', {'form': form})
    else:
        form = CourseRequestForm()
    return render(request, 'courserequest/courseRequest.html', {'form': form})


def login(request):
    return render(request, 'transferGuideApp/login.html')

class NewsView(generic.ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'transferguideApp/news.html'
    
class ViewCourseRequestView(generic.ListView):
    model = News
    context_object_name = 'course_request_list'
    template_name = 'transferguideApp/viewcourserquest.html'

    def get_queryset(self):
        # returns the latest news
        return News.objects.all()
