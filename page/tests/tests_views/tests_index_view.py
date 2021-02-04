from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, AnonymousUser


class IndexTestCase(TestCase):
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

    def test_index_without_authenticate(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

    def test_index_with_authenticate_without_group(self):
        self.client.force_login(self.user)
        response = self.client.get('/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

    def test_index_with_authenticate_as_admin_without_other_groups(self):
        self.user.groups.add(self.groups['administracja'])
        self.client.force_login(self.user)
        response = self.client.get('/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 3)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/o/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[2][0], '/')
        self.assertEqual(response.redirect_chain[2][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

    def test_index_with_authenticate_as_admin_with_other_groups(self):
        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.get('/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/admin_orders.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/orders/1/a/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.user.groups.remove(self.groups['4dich'])

        self.user.groups.add(self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.get('/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/admin_orders.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/orders/1/a/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.user.groups.remove(self.groups['besart'])

        self.user.groups.add(self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.get('/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/admin_orders.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/orders/1/a/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.user.groups.remove(self.groups['kasia'])

        self.user.groups.add(self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.get('/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/admin_orders.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/orders/1/a/')
        self.assertIsInstance(response.wsgi_request.user, User)

    def test_index_with_authenticate_as_druk(self):
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.get('/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_orders.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/u/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/orders/1/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.user.groups.remove(self.groups['4dich'])
