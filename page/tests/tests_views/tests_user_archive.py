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

    def test_user_archive_without_authentication(self):
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/orders/archive/1/u/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

    def test_user_archive_with_authentication_as_user_without_groups(self):
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

    def test_user_archive_with_authentication_as_user_with_wrong_group(self):
        self.user.groups.add(self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)
        self.user.groups.remove(self.groups['4dich'])

        self.user.groups.add(self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)
        self.user.groups.remove(self.groups['besart'])

        self.user.groups.add(self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)
        self.user.groups.remove(self.groups['kasia'])

        self.user.groups.add(self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

    def test_user_archive_with_authentication_as_user_with_administracja_group(self):
        self.user.groups.add(self.groups['administracja'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertIsInstance(response.wsgi_request.user, AnonymousUser)

    def test_user_archive_with_proper_authentication(self):
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/1/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.user.groups.remove(self.groups['druk'])

        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/1/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.user.groups.remove(self.groups['4dich'])

        self.user.groups.add(self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/1/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.user.groups.remove(self.groups['besart'])

        self.user.groups.add(self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/1/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.user.groups.remove(self.groups['kasia'])

        self.user.groups.add(self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/1/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.user.groups.remove(self.groups['Pomoc techniczna'])

    def test_user_archive_with_administracja_and_druk_group(self):
        self.user.groups.add(self.groups['administracja'], self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/1/u/')
        self.assertIsInstance(response.wsgi_request.user, User)

    def test_user_archive_with_2_as_current_page(self):
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/2/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/orders/archive/1/u/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/1/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.assertEqual(response.context[0]['archive_order_list'].count(), 0)

        for i in range(40):
            order = ActiveOrder(owner=self.groups['4dich'], order_number=i, image=i, divided='całe', tracking_number=i,
                                pub_date=date.today(), order_status='4')
            order.save()

        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/2/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/2/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.assertEqual(response.context[0]['archive_order_list'].count(), 15)
        self.assertEqual(response.context[0]['prev_page'], 1)
        self.assertEqual(response.context[0]['next_page'], 3)

        self.user.groups.remove(self.groups['druk'])
        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/2/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/2/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.assertEqual(response.context[0]['archive_order_list'].count(), 15)

        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/2/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/2/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.assertEqual(response.context[0]['archive_order_list'].count(), 15)
        self.assertEqual(response.context[0]['prev_page'], 1)
        self.assertEqual(response.context[0]['next_page'], 3)

        self.user.groups.remove(self.groups['4dich'])
        self.user.groups.add(self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/1/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.assertEqual(response.context[0]['archive_order_list'].count(), 15)
        self.assertEqual(response.context[0]['prev_page'], 0)
        self.assertEqual(response.context[0]['next_page'], 2)

        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/2/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/2/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.assertEqual(response.context[0]['archive_order_list'].count(), 15)
        self.assertEqual(response.context[0]['prev_page'], 1)
        self.assertEqual(response.context[0]['next_page'], 3)

        self.user.groups.remove(self.groups['Pomoc techniczna'])
        self.user.groups.add(self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/1/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.assertEqual(response.context[0]['archive_order_list'].count(), 0)
        self.assertEqual(response.context[0]['prev_page'], 0)
        self.assertEqual(response.context[0]['next_page'], 0)

        self.user.groups.remove(self.groups['kasia'])
        self.user.groups.add(self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.get('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/orders/archive/1/u/')
        self.assertIsInstance(response.wsgi_request.user, User)
        self.assertEqual(response.context[0]['archive_order_list'].count(), 0)
        self.assertEqual(response.context[0]['prev_page'], 0)
        self.assertEqual(response.context[0]['next_page'], 0)

    def test_user_archive_post_method_without_authentication(self):
        response = self.client.post('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/orders/archive/1/u/')
        self.assertEqual(response.redirect_chain[0][1], 302)

    def test_user_archive_post_method_with_authentication(self):
        self.client.force_login(self.user)
        response = self.client.post('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)

    def test_user_archive_post_method_with_authentication_as_proper_group(self):
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.post('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.user.groups.remove(self.groups['4dich'])
        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.post('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.user.groups.remove(self.groups['4dich'])

        self.user.groups.add(self.groups['administracja'], self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.post('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.user.groups.remove(self.groups['besart'])

        self.user.groups.add(self.groups['administracja'], self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.post('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.user.groups.remove(self.groups['kasia'])

        self.user.groups.add(self.groups['administracja'], self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.post('/orders/archive/1/u/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/user_archive.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
