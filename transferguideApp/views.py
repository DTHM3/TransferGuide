
from django.shortcuts import render, redirect

from django.shortcuts import render

from transferguideApp.models import UVAClass
import requests

from django.http import JsonResponse 
from django.shortcuts import render

from .forms import CourseRequestForm
from transferguideApp.models import UVAClass, News
from .models import CourseRequest


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
        keywordURL = f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&page=1&keyword={search_value}"
        numURL = f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&page=1&class_nbr={search_value}"

        if (search_type == "subject"):
            url = subjectURL
        elif (search_type == "professor"):
            url = instructorURL
        elif (search_type == "keyword"):
            url = keywordURL
        elif (search_type == "class-number"):
            url = numURL
        # print(url)
        response = requests.get(url)
        response = response.json()
        print(response)

        for item in response:
            myclass = UVAClass()
            myclass.class_id = item['crse_id'] + '-' + str(item['crse_offer_nbr'])
            myclass.subject = item['subject']
            myclass.class_description = item['descr']
            myclass.instructors = item['instructors'][0]['name'] + ', ' + item['instructors'][0]['email']
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
            return redirect('list_course_requests')  # To change after
        else:
            return render(request, 'courserequest/courseRequest.html', {'form': form})
    else:
        form = CourseRequestForm()
    return render(request, 'courserequest/courseRequest.html', {'form': form})


def course_equivalency(request):
    return render(request, 'transferguideApp/courseEquivalency.html')


def login(request):
    return render(request, 'transferguideApp/login.html')

# class NewsView(generic.ListView):
#     model = News
#     context_object_name = 'news_list'
#     template_name = 'transferguideApp/news.html'
    
#     def get_queryset(self):
#         # returns the latest news
#         return News.objects.all()

def news_index(request):
    news = News.objects.all()
    return render(request, 'transferguideApp/news_index.html', {'news': news})

def news_detail(request, title):
    news = News.objects.get(title=title)
    return render(request, 'transferguideApp/news_detail.html', {'news': news})

# SOURCE: https://stackoverflow.com/questions/15636527/django-model-object-filter
def list_course_requests(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_staff:
        course_requests = CourseRequest.objects.all().order_by('id')
    else:
        course_requests = CourseRequest.objects.filter(user=request.user).order_by('id')
    return render(request, 'courserequest/list_course_requests.html', {'course_requests': course_requests})

# SOURCE: https://stackoverflow.com/questions/19132210/what-does-request-method-post-mean-in-django 
def course_request_detail(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    course_request = CourseRequest.objects.get(id=id)

    if request.method == 'POST':
        course_request.status = request.POST['status']
        course_request.course_equivalency = request.POST['course_equivalency']
        course_request.save()
        return redirect('list_course_requests')

    return render(request, 'courserequest/course_request_detail.html', {'course_request': course_request})

# SOURCE: https://stackoverflow.com/questions/37205793/django-values-list-vs-values
def course_equivalency(request):
    if not request.user.is_authenticated:
        return redirect('login')
    institutions = set(CourseRequest.objects.values_list('transfer_institution', flat=True))
    courses = CourseRequest.objects.all().order_by('transfer_institution')

    if request.GET.get('transfer_institution'):
        courses = courses.filter(transfer_institution=request.GET['transfer_institution'])

    return render(request, 'courserequest/course_equivalency.html', {'courses': courses, 'institutions': institutions})