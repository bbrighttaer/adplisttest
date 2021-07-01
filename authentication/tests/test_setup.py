from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker

class TestSetup(APITestCase):
    
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.fake = Faker()

        self.user_data = {
            'title': 'Mr',
            'email': self.fake.email(),
            'username': self.fake.name(),
            'password': '@Admin123',
            'firstName': self.fake.name(),
            'lastName': self.fake.name(),
            'location': 'Accra',
            'employer': self.fake.company(),
            'joined_as': 'mentor',
            'expertise': ['UI/UX Design'],
            'mentorship_areas': ['Career Advice']
        }
        return super().setUp()


    def tearDown(self):
        return super().tearDown()