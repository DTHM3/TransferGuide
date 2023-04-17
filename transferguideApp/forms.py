from django import forms
from django.forms import ModelForm
from .models import CourseRequest

# Citation: how to validate url using django
# https://stackoverflow.com/questions/3170231/how-can-i-check-if-a-url-exists-with-django-s-validators
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class CourseRequestForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('This field is required')
        return title

    def clean_credits(self):
        credits = self.cleaned_data.get('credits')
        if credits < 1 or credits > 6:
            raise forms.ValidationError('Please enter a valid number of credits')
        return credits

    def clean_url(self):
        url = self.cleaned_data.get('url')
        validator = URLValidator()
        try:
            validator(url)
            return True
        except ValidationError:
            raise forms.ValidationError('Please enter a valid url for your institution')

    def clean_transfer_institution(self):
        transfer_institution = self.cleaned_data.get('transfer_institution')
        if len(transfer_institution) < 5:
            raise forms.ValidationError('Please enter a valid transfer institution')
        return transfer_institution

    def clean_course_subject(self):
        course_subject = self.cleaned_data.get('course_subject')
        if len(course_subject) < 3:
            raise forms.ValidationError('Please enter a valid course subject')
        return course_subject

    def clean(self):
        cleaned_data = super(CourseRequestForm, self).clean()
        cleaned_data.get('title')
        cleaned_data.get('course_subject')
        cleaned_data.get('credits')
        cleaned_data.get('transfer_institution')
        cleaned_data.get('url')
        return cleaned_data

    class Meta:
        model = CourseRequest
        fields = ['title', 'course_subject', 'credits', 'transfer_institution', 'url']
        exclude = ['status', 'user']



        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'course_subject': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.TextInput(attrs={'class': 'form-control'}),
            'transfer_institution': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }


