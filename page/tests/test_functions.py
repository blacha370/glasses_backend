from django.test import TestCase
from django.contrib.auth.models import User, AnonymousUser
from ..functions import *
from ..models import ActiveOrder


class ValidateAccessTestCase(TestCase):
    def setUp(self):
        self.user = User(username='User', password='password')
        self.user.save()
        names = ['administracja', 'druk', '4dich', 'besart', 'kasia', 'Pomoc techniczna']
        self.groups = {}
        for name in names:
            group = Group(name=name)
            group.save()
            self.groups[name] = group
        self.order = ActiveOrder(owner=self.groups['4dich'], order_number='1312324124124124', pub_date=date.today())
        self.order.save()

    def test_without_authenticated_user(self):
        self.assertFalse(validate_acces(AnonymousUser(), self.order))
