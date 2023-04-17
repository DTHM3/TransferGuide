from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from transferguideApp.forms import CourseRequestForm
from transferguideApp.models import UVAClass, CourseRequest

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class CourseRequestDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client.login(username='test', password='test')
        self.url = reverse('course-request')
        form_data = {
            'title': 'Test Course Request',
            'course_subject': 'Test Subject',
            'credits': 3,
            'transfer_institution': 'Test Institution',
            'url': 'https://www.test.com',
        }
        response = self.client.post(self.url, data=form_data)
        self.url = reverse('course_request_detail', args=['1'])

    def test_attempt_to_view_course_request_noAuthentication(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'))

    def test_validRequestDetail(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'courserequest/course_request_detail.html')
        self.assertEqual(response.context['course_request'].title, 'Test Course Request')
        self.assertEqual(response.context['course_request'].course_subject, 'Test Subject')
        self.assertEqual(response.context['course_request'].credits, 3)
        self.assertEqual(response.context['course_request'].transfer_institution, 'Test Institution')
        self.assertEqual(response.context['course_request'].url, 'https://www.test.com')


class ListCourseRequestsViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.url = reverse('list_course_requests')

    def test_attempt_to_view_course_request_noAuthentication(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'))

    def test_lists_all_course_requests_by_submitter(self):
        self.client.login(username='test', password='test')
        self.url = reverse('course-request')
        form_data = {
            'title': 'Test Course Request',
            'course_subject': 'Test Subject',
            'credits': 3,
            'transfer_institution': 'Test Institution',
            'url': 'https://www.test.com',
        }
        response = self.client.post(self.url, data=form_data)
        self.url = reverse('list_course_requests')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'courserequest/list_course_requests.html')
        self.assertEqual(len(response.context['course_requests']), 1)
        self.assertEqual(response.context['course_requests'][0].user, self.user)
        self.assertEquals(response.context['course_requests'][0].title, 'Test Course Request')


class CourseRequestViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.url = reverse('course-request')

    def test_attempt_to_submit_course_request_noAuthentication(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'))

    def test_get_request_returns_valid_form(self):
        self.client.login(username='test', password='test')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'courserequest/courseRequest.html')
        self.assertIsInstance(response.context['form'], CourseRequestForm)

    def test_valid_form_submission_creates_new_CourseRequest(self):
        self.client.login(username='test', password='test')
        form_data = {
            'title': 'Test Course Request',
            'course_subject': 'Test Subject',
            'credits': 3,
            'transfer_institution': 'Test Institution',
            'url': 'https://www.test.com',
        }
        response = self.client.post(self.url, data=form_data)
        self.assertRedirects(response, reverse('list_course_requests'))
        self.assertEqual(CourseRequest.objects.count(), 1)
        self.assertEqual(CourseRequest.objects.first().user, self.user)

    def test_invalid_form_submission_creates_new_CourseRequest(self):
        self.client.login(username='test', password='test')
        form_data = {
            'title': 'Test Course Request',
            'course_subject': 'Test Subject',
            'credits': 3,
            'transfer_institution': 'Test Institution',
            'url': 'invalid brrrrr',
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(CourseRequest.objects.count(), 0)
        self.assertTemplateUsed(response, 'courserequest/courseRequest.html')


class TestSearchViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.client.login(username='test', password='test')

    def test_get_search(self):
        response = self.client.get(reverse('search'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'transferguideApp/search.html')

    def test_post_search_good_search(self):
        uvaClass = UVAClass(
            class_id='046231',
            subject='CS',
            class_description='Software Development Essentials',
            instructors=[{'name': 'Paul McBurney', 'email': 'pm8fc@virginia.edu'}],
            units=3
        )
        response = self.client.post(
            reverse('search'),
            {
                'searchType': 'professor',
                'search': 'McBurney'
            }
        )

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'transferguideApp/search.html')
        self.assertEquals(response.context['classes'][0].instructors, uvaClass.instructors)

    # todo: Maybe our responnse should not really be like this
    def test_post_search_bad_search(self):
        uvaClass = UVAClass(
            class_id='046231',
            subject='CS',
            class_description='Software Development Essentials',
            instructors=[{'name': 'Paul McBurney', 'email': 'pm8fc@virginia.edu'}],
            units=3
        )
        response = self.client.post(
            reverse('search'),
            {
                'searchType': 'professor',
                'search': 'edjifjieafjiaedjiaedjideaj'
            }
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'transferguideApp/search.html')
        self.assertEquals(response.context['classes'], [])
