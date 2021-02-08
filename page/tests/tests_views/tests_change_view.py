from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from ...models import ActiveOrder
from datetime import date


class ChangeTestCase(TestCase):
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
        response = self.client.get('/change/1/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/change/1/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(self.order.order_status, '1')

    def test_with_not_existing_order(self):
        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.get('/change/2/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/orders/1/a/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_orders.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
