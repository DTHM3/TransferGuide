from django import forms
from django.forms import ModelForm
from .models import CourseRequest


class CourseRequestForm(forms.ModelForm):
    class Meta:
        model = CourseRequest
        fields = ['title', 'course_subject', 'credits', 'transfer_institution', 'url']
        exclude = ['status']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'course_subject': forms.TextInput(attrs={'class': 'form-control'}),
            'credits': forms.TextInput(attrs={'class': 'form-control'}),
            'transfer_institution': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
        }

