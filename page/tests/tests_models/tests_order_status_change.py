from django.test import TestCase
from django.db.utils import IntegrityError
from django.db.transaction import atomic
from django.contrib.auth.models import Group, User
import datetime
from ...models import OrderStatusChange, ActiveOrder


class OrderStatusChangeTestCase(TestCase):
    def setUp(self):
        names = ['z4l', 'besart', 'kasia', 'administracja', 'Pomoc techniczna', 'druk']
        for name in names:
            group = Group(name=name)
            group.save()
        self.user = User(username='User')
        self.user.save()
        self.groups = Group.objects.all()
        self.active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234',
                                        order_status=ActiveOrder.order_statuses[0], image='000', divided='całe',
                                        tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        self.active_order.save()

    def test_create_order_status_change(self):
        status_change = OrderStatusChange(order=self.active_order, change_owner=self.user,
                                          previous_state=self.active_order.order_status,
                                          new_state=ActiveOrder.order_statuses[1])
        status_change.save()
        self.assertEqual(status_change.order, self.active_order)
        self.assertEqual(status_change.change_owner, self.user)
        self.assertEqual(status_change.previous_state, ActiveOrder.order_statuses[0])
        self.assertEqual(status_change.new_state, ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 1)

    def test_create_order_status_change_with_string_as_order(self):
        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order='', change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=' ', change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order='\n ', change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order='order', change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order='1', change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_order_status_change_with_int_as_order(self):
        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=1, change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=0, change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=-1, change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_order_status_change_with_float_as_order(self):
        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=1.1, change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=-1.1, change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_order_status_change_with_bool_as_order(self):
        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=True, change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=False, change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_order_status_change_with_none_as_order(self):
        with atomic():
            status_change = OrderStatusChange(order=None, change_owner=self.user,
                                              previous_state=self.active_order.order_status,
                                              new_state=ActiveOrder.order_statuses[1])
            self.assertRaises(IntegrityError, status_change.save)
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_order_status_change_with_structure_as_order(self):
        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=list(), change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=dict(), change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=tuple(), change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=set(), change_owner=self.user,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_order_status_change_without_order(self):
        with atomic():
            status_change = OrderStatusChange(change_owner=self.user, previous_state=self.active_order.order_status,
                                              new_state=ActiveOrder.order_statuses[1])
            self.assertRaises(IntegrityError, status_change.save)
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_with_string_as_change_owner(self):
        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner='',
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=' ',
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner='\n ',
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner='user',
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_with_int_as_change_owner(self):
        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=1,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=0,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=-1,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_with_float_as_change_owner(self):
        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=1.1,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=-1.1,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_with_bool_as_change_owner(self):
        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=True,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=False,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_with_none_as_change_owner(self):
        with atomic():
            status_change = OrderStatusChange(order=self.active_order, change_owner=None,
                                              previous_state=self.active_order.order_status,
                                              new_state=ActiveOrder.order_statuses[1])
            self.assertRaises(IntegrityError, status_change.save)
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_with_structure_as_change_owner(self):
        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=list(),
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=dict(),
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=tuple,
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

        with atomic():
            self.assertRaises(ValueError, OrderStatusChange, order=self.active_order, change_owner=set(),
                              previous_state=self.active_order.order_status, new_state=ActiveOrder.order_statuses[1])
        self.assertEqual(OrderStatusChange.objects.count(), 0)

    def test_create_without_change_owner(self):
        with atomic():
            status_change = OrderStatusChange(order=self.active_order, previous_state=self.active_order.order_status,
                                              new_state=ActiveOrder.order_statuses[1])
            self.assertRaises(IntegrityError, status_change.save)
        self.assertEqual(OrderStatusChange.objects.count(), 0)
