# registration/tests.py

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.contrib.auth.hashers import make_password, check_password
from registration.models import BusinessOwner

class BusinessOwnerModelTest(TestCase):

    def test_password_hashing_on_save(self):
        # Test that password is hashed on save
        business_owner = BusinessOwner(name="John Doe", email="john@example.com", password="Password123")
        business_owner.save()
        self.assertTrue(check_password("Password123", business_owner.password))

    def test_check_password(self):
        # Test the check_password method
        business_owner = BusinessOwner(name="Jane Doe", email="jane@example.com", password="SecurePass1")
        business_owner.save()
        self.assertTrue(business_owner.check_password("SecurePass1"))
        self.assertFalse(business_owner.check_password("WrongPassword"))

    def test_save_with_already_hashed_password(self):
        # Test that an already hashed password is not hashed again
        hashed_password = make_password("AlreadyHashedPassword")
        business_owner = BusinessOwner(name="Alice", email="alice@example.com", password=hashed_password)
        business_owner.save()
        self.assertEqual(business_owner.password, hashed_password)
