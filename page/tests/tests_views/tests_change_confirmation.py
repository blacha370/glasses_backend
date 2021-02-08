from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from ...models import ActiveOrder
from datetime import date


class ChangeConfirmationTestCase(TestCase):
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
        self.order = ActiveOrder(owner=self.groups['4dich'], order_number=1, pub_date=date.today(), order_status='1',
                                 image='00001', divided='całe', tracking_number=1)
        self.order.save()

    def test_without_authentication(self):
        response = self.client.get('/change_confirmed/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/change_confirmed/1/1')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(ActiveOrder.objects.get(pk=1).order_status, '1')

        response = self.client.get('/change_confirmed/1/2', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/change_confirmed/1/2')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(ActiveOrder.objects.get(pk=1).order_status, '1')

    def test_with_authentication_without_groups(self):
        self.client.force_login(self.user)
        response = self.client.get('/change_confirmed/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(ActiveOrder.objects.get(pk=1).order_status, '1')

        self.client.force_login(self.user)
        response = self.client.get('/change_confirmed/1/2', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(ActiveOrder.objects.get(pk=1).order_status, '1')

    def test_with_authentication_as_administracja_group(self):
        self.user.groups.add(self.groups['administracja'])
        self.client.force_login(self.user)
        response = self.client.get('/change_confirmed/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(ActiveOrder.objects.get(pk=1).order_status, '1')

        self.client.force_login(self.user)
        response = self.client.get('/change_confirmed/1/2', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(ActiveOrder.objects.get(pk=1).order_status, '1')
