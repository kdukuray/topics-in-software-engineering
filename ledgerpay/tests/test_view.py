from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from payments.models import Transaction


class DashboardViewTest(TestCase):
    """ In this test i will try to create users and try to do stuff that requires login
    to see if when they hit dashboard which is protected by a login_required if they are receving the 
    right response"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create 2 transactions for that user
        Transaction.objects.create(
            associated_user=self.user,
            amount=100,
        )
        Transaction.objects.create(
            associated_user=self.user,
            amount=200,
        )
        #  URL 
        self.dashboard_url = reverse('dashboard')  
    
    def test_dashboard_logged_in_user_can_access(self):
        """
        Test that a logged-in user can access the dashboard,
        and only sees their own transactions.
        """
        #login
        self.client.login(username='testuser', password='testpass')

        response = self.client.get(self.dashboard_url)

        # Check 200 OK response
        self.assertEqual(response.status_code, 200)
        
        # template
        self.assertTemplateUsed(response, 'payments/dashboard.html')

        # the returned transactions belong to "testuser" and btw we created 2 transact
        transactions = response.context['transactions'] 
        self.assertEqual(transactions.count(), 2)
        

    def test_dashboard_redirects_when_not_logged_in(self):
        """
        Test that an unauthenticated user is redirected to the login URL.
        """
        response = self.client.get(self.dashboard_url)

        # Because of @login_required(login_url="login"), it shouldn't work->error
        self.assertEqual(response.status_code, 302)
        
        #now let s see if they go back to /login 
        self.assertIn('/login', response.url)
        
