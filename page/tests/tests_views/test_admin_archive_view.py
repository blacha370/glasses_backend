from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, AnonymousUser
from ...models import ActiveOrder
from datetime import date


class AdminOrdersTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(username='User', password='password')
        self.user.save()
        names = ['administracja', 'druk', '4dich', 'besart', 'kasia', 'Pomoc techniczna']
        self.groups = {}
        for name in names:
            group = Group(name=name)
            group.save()
            self.groups[name] = group

    def test_admin_orders_without_authentication(self):
        response = self.client.get('/orders/archive/1/a/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/orders/archive/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

    def test_admin_orders_with_authentication_as_user_without_groups(self):
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/a/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)
