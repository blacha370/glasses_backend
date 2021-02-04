from django.test import TestCase, Client
from django.contrib.auth.models import User, AnonymousUser


class LogoutUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(username='User', password='password')
        self.user.save()

    def test_logout_without_authentication(self):
        response = self.client.get('/o/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

    def test_logout_with_authentication(self):
        self.client.force_login(self.user)
        response = self.client.get('/o/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)
