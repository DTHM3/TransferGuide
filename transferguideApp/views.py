from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from django.shortcuts import render
from transferguideApp.models import UVAClass
import requests

import requests
from django.http import JsonResponse
from django.shortcuts import render
import json
from transferguideApp.models import UVAClass

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
