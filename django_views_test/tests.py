from django.test import TestCase
from django.test import Client

class LoginTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login(self):
        response = self.client.get('/login')
        assert response.status_code == 200
        pass

