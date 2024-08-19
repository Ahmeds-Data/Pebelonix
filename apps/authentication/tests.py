# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Ahmed Salim
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from apps.authentication.models import Profile

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        self.register_url = reverse('register')

    def test_user_registration_creates_profile(self):
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username=self.user_data['username'])
        self.assertIsNotNone(user)
        profile_exists = Profile.objects.filter(user=user).exists()
        self.assertTrue(profile_exists)

    def test_user_registration_creates_authenticated_user(self):
        self.client.post(self.register_url, data=self.user_data)
        user = authenticate(username=self.user_data['username'], password=self.user_data['password1'])
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)

    

