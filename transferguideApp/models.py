from django.db import models


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


class CourseRequest(models.Model):
    title = models.CharField(max_length=200)
    course_subject = models.CharField(max_length=200)
    credits = models.IntegerField()
    transfer_institution = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
