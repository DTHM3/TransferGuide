from django.contrib.auth.models import User
from django.test import TestCase
from oauthlib.oauth1 import Client

from .models import UVAClass

class ClassSearchTest(TestCase):
    results = []

    def setUp(self):
        self.user = User.objects.create_user(username='jdoe', password='jdoepass')
        self.client.login(username='jdoe', password='jdoepass')

    def test_search_success(self):
        response = self.client.get("/guide/search/")
        self.assertContains(response, "id")


    def test_search_fail(self):
        response = self.client.get("/guide/search/")
        self.assertNotContains(response, "asdfjsd")

    def test_more(self):
       response = self.client.get("/guide/search/")
       self.assertTrue(self, True)

