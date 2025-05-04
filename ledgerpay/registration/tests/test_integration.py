# registration/tests/test_integration.py
from django.test import TestCase
from django.urls import reverse
from registration.models import BusinessOwner

class RegistrationIntegrationTests(TestCase):
    def test_successful_registration(self):
        # Test that a business owner can be successfully registered
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'Password123',
        }
        response = self.client.post(reverse('register'), data)

        # Check if the response is a success and if the business owner is created
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Registration successful!")
        self.assertTrue(BusinessOwner.objects.filter(email='john@example.com').exists())

    def test_duplicate_email_registration(self):
        # Test that attempting to register with a duplicate email fails
        # Create a business owner with the email already in the database
        BusinessOwner.objects.create(
            name='Jane Doe', 
            email='john@example.com', 
            password='Password123'
        )

        data = {
            'name': 'John Doe',
            'email': 'john@example.com',  # Duplicate email
            'password': 'Password123',
        }
        response = self.client.post(reverse('register'), data)

        # Check for the error message in the rendered HTML page
        self.assertEqual(response.status_code, 200)  # Expecting 200 OK because it's an HTML page
        self.assertContains(response, "Email already exists")
        self.assertEqual(BusinessOwner.objects.filter(email='john@example.com').count(), 1)  # Only one should exist
