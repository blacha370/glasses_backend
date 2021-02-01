from django.test import TestCase
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
