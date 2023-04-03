from django.test import TestCase

from .models import UVAClass


# class ClassSearchTest(TestCase):
#     results = []

#     def setUp(self):
#         self.results.append(UVAClass.objects.create(class_id="test", subject="test subject",
#                                                     class_description="test desc",
#                                                     instructors={'name': "test name", "email": "test email"}, units=3))

#     def test_search_success(self):
#         response = self.client.get("/guide/search/")
#         self.assertContains(response, "id")
#     def test_search_fail(self):
#         response = self.client.get("/guide/search/")
#         self.assertNotContains(response, "asdfjsd")

#     def test_more(self):
#        response = self.client.get("/guide/search/")
#        self.assertTrue(self, True)
