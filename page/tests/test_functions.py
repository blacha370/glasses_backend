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
        self.assertFalse(validate_access(AnonymousUser(), self.order))

    def test_with_authentication_without_group(self):
        self.assertFalse(validate_access(self.user, self.order))

    def test_with_authentication_with_wrong_group(self):
        self.user.groups.add(self.groups['druk'])
        self.assertFalse(validate_access(self.user, self.order))

        self.user.groups.remove(self.groups['druk'])
        self.user.groups.add(self.groups['administracja'])
        self.assertFalse(validate_access(self.user, self.order))

        self.user.groups.add(self.groups['besart'])

        self.assertFalse(validate_access(self.user, self.order))

        self.user.groups.remove(self.groups['besart'])
        self.user.groups.add(self.groups['kasia'])
        self.assertFalse(validate_access(self.user, self.order))
