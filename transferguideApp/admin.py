from django.contrib import admin
from .models import UVAClass, News, CourseRequest

# Register Custom models here.
# SOURCEs: https://juhanajauhiainen.com/posts/customize-django-admin-with-list-display-property
class CourseRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'status')


admin.site.register(UVAClass)
admin.site.register(News)
admin.site.register(CourseRequest, CourseRequestAdmin)
