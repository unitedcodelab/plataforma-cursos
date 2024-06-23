from django.test import TestCase, Client
from django.urls import reverse
from apps.entities.models import Student
from django.contrib.auth.models import User
from unittest.mock import patch


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.student = Student.objects.create(user=self.user, verified=True)
        self.url = reverse('home')


    def test_valid(self):
        self.client.login(username='testuser', password='password')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    
    def test_not_authenticated(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/home')

    
    def test_not_allowed_methods(self):
        self.client.login(username='testuser', password='password')
        
        response_post = self.client.post(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)
        responses = [response_post, response_put, response_delete]

        for response in responses:
            self.assertEqual(response.status_code, 405)
            self.assertTemplateNotUsed(response, 'home.html')
    