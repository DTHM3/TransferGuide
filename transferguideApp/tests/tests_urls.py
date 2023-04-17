from django.test import SimpleTestCase
from django.urls import resolve, reverse

from transferguideApp.views import login, render_template, course_request, list_course_requests, course_request_detail, news_index


# Everytime we do not need to interact with database
class TestUrls(SimpleTestCase):

    def test_login_url(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)

    def test_home_url(self):
        url = reverse('home')
        self.assertEquals(resolve(url).view_name, "home")

    def test_search_url(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, render_template)

    def test_course_request_url(self):
        url = reverse('course-request')
        self.assertEquals(resolve(url).func, course_request)

    #
    def test_course_request_list_url(self):
        url = reverse('list_course_requests')
        self.assertEquals(resolve(url).func, list_course_requests)

    def test_course_request_detail_url(self):
        url = reverse('course_request_detail', args=['1'])
        self.assertEquals(resolve(url).func, course_request_detail)

    def test_news_list_url(self):
        url = reverse('news_index')
        self.assertEquals(resolve(url).func, news_index)
