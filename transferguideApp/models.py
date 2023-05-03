from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UVAClass(models.Model):
    class_id = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    class_description = models.TextField()
    instructors = models.JSONField()
    units = models.IntegerField()


class News(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    date = models.DateTimeField('date published')
    img_src = models.CharField(max_length=300, default="images/transfer.png")

# SOURCES: 
# https://stackoverflow.com/questions/18676156/how-to-properly-use-the-choices-field-option-in-django
# https://www.scaler.com/topics/django/Django-foreign-key/

class CourseRequest(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    course_subject = models.CharField(max_length=200)
    credits = models.IntegerField()
    transfer_institution = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied'),
    )
    course_equivalency = models.CharField(max_length=200, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="NO USER") 

