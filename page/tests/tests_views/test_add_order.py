from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from ...models import ActiveOrder


class AddOrderTestCase(TestCase):
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

    def test_upload_file(self):
        self.user.groups.add(self.groups['administracja'], self.groups['Pomoc techniczna'])
        with open('data_for_tests.csv') as file:
            self.client.force_login(self.user)
            response = self.client.post('/add/order/', {'name': 'fred', 'file': file}, follow=True)
            self.assertEqual(response.templates[0].name, 'page/admin_orders.html')
            self.assertEqual(response.templates[1].name, 'page/base.html')
            self.assertEqual(len(response.redirect_chain), 1)
            self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
            self.assertEqual(response.redirect_chain[0][1], 302)
            self.assertEqual(ActiveOrder.objects.count(), 18)
            self.assertEqual(len(response.context[0]['active_order_list']), 15)
            self.assertEqual(response.context[0]['active_order_list'].model, ActiveOrder)
            for order in ActiveOrder.objects.all():
                self.assertEqual(order.owner, self.groups['besart'])

    def test_upload_file_without_authentication(self):
        with open('data_for_tests.csv') as file:
            response = self.client.post('/add/order/', {'name': 'fred', 'file': file}, follow=True)
            self.assertEqual(response.templates[0].name, 'page/index.html')
            self.assertEqual(response.templates[1].name, 'page/base.html')
            self.assertEqual(len(response.redirect_chain), 1)
            self.assertEqual(response.redirect_chain[0][0], '/?next=/add/order/')
            self.assertEqual(response.redirect_chain[0][1], 302)
            self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_upload_file_as_druk_group(self):
        self.user.groups.add(self.groups['druk'])
        with open('data_for_tests.csv') as file:
            self.client.force_login(self.user)
            response = self.client.post('/add/order/', {'name': 'fred', 'file': file}, follow=True)
            self.assertEqual(response.templates[0].name, 'page/user_orders.html')
            self.assertEqual(response.templates[1].name, 'page/base.html')
            self.assertEqual(len(response.redirect_chain), 1)
            self.assertEqual(response.redirect_chain[0][0], '/orders/1/u/')
            self.assertEqual(response.redirect_chain[0][1], 302)
            self.assertEqual(ActiveOrder.objects.count(), 0)
            self.assertEqual(len(response.context[0]['active_order_list']), 0)

    def test_upload_file_get_method_without_authentication(self):
        response = self.client.get('/add/order/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/add/order/')
        self.assertEqual(response.redirect_chain[0][1], 302)

    def test_upload_file_get_method_with_authentication(self):
        self.client.force_login(self.user)
        response = self.client.get('/add/order/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 3)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/o/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[2][0], '/')
        self.assertEqual(response.redirect_chain[2][1], 302)
