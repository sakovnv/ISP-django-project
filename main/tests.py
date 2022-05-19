from django.urls import reverse

from main.models import User, Category, Ad
from django.test import TestCase


class TestUser(TestCase):
    fixtures = ['users.json', 'categories.json', 'ads.json']

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('test_user', email=None, password='testpass')

    def test_get_user(self):
        user = User.objects.get(username='test_user')
        self.assertTrue(user.check_password('testpass'))

    def test_main_view(self):
        response = self.client.get(f'')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_ad_absolute_url(self):
        ad = Ad.objects.get(pk=1)
        self.assertEqual(ad.get_absolute_url(), '/ad/1')

    def test_ad_view(self):
        response = self.client.get(reverse('ad', kwargs={'ad_id': '1'}))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        login = self.client.login(username='test_user', password='testpass')
        self.client.logout()
