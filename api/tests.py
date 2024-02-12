from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Restaurant, Ticket, Shelter, FoodInspector, Volunteer, Organizer, ShelterRequest
from datetime import date

# Create your tests here.

class APITEST(TestCase):
    def setUp(self):
        self.client = APIClient()
         
    def test_restaurant_signup(self):
        
        response = self.client.post('/signup/restaurant/', {
            'user': {
                'username': 'restaurant',
                'password': 'restaurant'
            }, 
            'name': 'restaurant',
            'email': 'restaurant@gmail.com',
            'phone_number': '914304530',
            'address': 'test',
            'concept': 'test'
        }, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_inspector_signup(self):            
            response = self.client.post('/signup/inspector/', {
                'user': {
                    'username': 'inspector',
                    'password': 'inspector'
                }, 
                'first_name': 'test',
                'last_name': 'test',
                'email': 'test',
                'phone_number': 'test'
            }, format='json')
            self.assertEqual(response.status_code, 201)
    
    def test_shelter_signup(self):
            response = self.client.post('/signup/shelter/', {
                'user': {
                    'username': 'shelter',
                    'password': 'shelter'
                }, 
                'name': 'test',
                'email': 'test',
                'phone_number': 'test',
                'address': 'test'
            }, format='json')
            self.assertEqual(response.status_code, 201)
    
    def test_volunteer_signup(self):
            response = self.client.post('/signup/volunteer/', {
                'user': {
                    'username': 'volunteer',
                    'password': 'volunteer'
                }, 
                'first_name': 'test',
                'last_name': 'test',
                'email': 'test',
                'phone_number': 'test'
            }, format='json')
            self.assertEqual(response.status_code, 201)
    
    def test_organizer_signup(self):
            response = self.client.post('/signup/organizer/', {
                'user': {
                    'username': 'organizer',
                    'password': 'organizer'
                }, 
                'first_name': 'test',
                'last_name': 'test',
                'email': 'test',
                'phone_number': 'test'
            }, format='json')
            self.assertEqual(response.status_code, 201) 

    

