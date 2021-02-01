from django.test import TestCase
from django.db.utils import IntegrityError
from django.db.transaction import atomic
from .models import *


class ActiveOrderTestCase(TestCase):
    def setUp(self):
        names = ['z4l', 'besart', 'kasia', 'administracja', 'Pomoc techniczna', 'druk']
        for name in names:
            group = Group(name=name)
            group.save()
        self.groups = Group.objects.all()

    def test_create_order(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

    def test_create_order_with_string_as_owner(self):
        self.assertRaises(ValueError, ActiveOrder, owner='', order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=' ', order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner='\n ', order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner='z4l', order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner='1', order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_int_as_owner(self):
        self.assertRaises(ValueError, ActiveOrder, owner=1, order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=0, order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=-1, order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_float_as_owner(self):
        self.assertRaises(ValueError, ActiveOrder, owner=1.1, order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=-1.1, order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_bool_as_owner(self):
        self.assertRaises(ValueError, ActiveOrder, owner=True, order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=False, order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_none_as_owner(self):
        with atomic():
            order = ActiveOrder(owner=None, order_number='QWERTYUIOP1234', pub_date='01.01.2020', order_status='1',
                                image='000', divided='całe', tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_structure_as_owner(self):
        self.assertRaises(ValueError, ActiveOrder, owner=list(), order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=dict(), order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=tuple(), order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=set(), order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                          order_status='1', image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_without_owner(self):
        with atomic():
            order = ActiveOrder(order_number='QWERTYUIOP1234', pub_date='01.01.2020', order_status='1', image='000',
                                divided='całe', tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_with_string_as_order_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number=' ', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, ' ')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='\n ', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '\n ')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='Order number', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'Order number')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

        active_order = ActiveOrder(owner=self.groups[0], order_number='Definitely too long order number',
                                   pub_date='01.01.2020', order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'Definitely too long order number')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 5)
