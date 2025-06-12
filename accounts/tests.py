from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render

class SignupTestCase(TestCase):
    
    #test for when all the data in the form is valid
    def test_with_valid_data(self):
        #simulate a post request
        response = self.client.post(reverse("signup"),{
            "username": "tom",
            "email": "me@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        })
        #check the user with the given username exists
        user_exists = User.objects.filter(username="tom").exists()
        self.assertTrue(user_exists)
        
        #check field values are correct
        user = User.objects.get(username="tom")
        self.assertEquals(user.email, "me@example.com")
        #check_password() because django hashes passwords
        self.assertTrue(user.check_password('StrongPass123'))
        
        #check that if signup successful, redirects to the login page
        self.assertRedirects(response,"/")

        #check that only a single user was created
        self.assertEqual(User.objects.count(), 1)

        #assert user is logged in after successful signup
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_password_mismatch(self):
        #simulate a post request
        response = self.client.post(reverse("signup"),{
            "username": "tom",
            "email": "me@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass12",
        })
        response.render()

        form = response.context['form']
        self.assertIn("The two password fields didn’t match.", form.errors.get('password2', []))