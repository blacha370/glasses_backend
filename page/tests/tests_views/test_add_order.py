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
