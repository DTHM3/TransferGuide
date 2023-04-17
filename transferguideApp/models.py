from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


curentUser = get_user_model()

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
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="NO USER") 
    
    def save(self, *args, **kwargs):
        if hasattr(self, 'user') and self.user.is_staff:
            self.status = 'Approved'
            super(CourseRequest, self).save(*args, **kwargs)
        else: 
            super(CourseRequest, self).save(*args, **kwargs)
    
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         print(User.is_staff)
    #         if User.is_staff:
    #             self.status = 'Approved'
    #         super(CourseRequest, self).save(*args, **kwargs)
    #     else: 
    #         super(CourseRequest, self).save(*args, **kwargs)

