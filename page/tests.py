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
        active_order = ActiveOrder.objects.get(order_number='')
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
        active_order = ActiveOrder.objects.get(order_number=' ')
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
        active_order = ActiveOrder.objects.get(order_number='\n ')
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
        active_order = ActiveOrder.objects.get(order_number='Order number')
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
        active_order = ActiveOrder.objects.get(order_number='Definitely too long order number')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'Definitely too long order number')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 5)

    def test_create_order_with_int_as_order_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number=1, pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=1)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '1')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number=0, pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=0)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '0')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number=-1, pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=-1)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '-1')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

    def test_create_order_with_bool_as_order_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number=True, pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=True)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'True')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number=False, pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=False)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'False')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_none_as_order_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number=None, pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        self.assertRaises(IntegrityError, active_order.save)

    def test_create_order_with_structure_as_order_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number=list(), pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=list())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '[]')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number=dict(), pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=dict())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '{}')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number=tuple(), pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=tuple())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '()')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number=set(), pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=set())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'set()')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_order_without_order_number(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], pub_date='01.01.2020', order_status='1', image='000',
                                       divided='całe', tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_string_as_pub_date(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date=' ',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, ' ')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='\n ',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '\n ')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', pub_date='date',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.pub_date, 'date')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1238', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1238')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 5)

    def test_create_order_with_int_as_pub_date(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date=1,
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(pub_date=1)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '1')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date=0,
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(pub_date=0)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '0')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date=-1,
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(pub_date=-1)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '-1')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

    def test_create_order_with_float_as_pub_date(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date=1.1,
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(pub_date=1.1)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '1.1')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date=-1.1,
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(pub_date=-1.1)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '-1.1')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_bool_as_pub_date(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date=True,
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(pub_date=True)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, 'True')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date=False,
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(pub_date=False)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, 'False')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_none_as_pub_date(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date=None,
                                       order_status='1', image='000', divided='całe',
                                       tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_structure_as_pub_date(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date=list(),
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(pub_date=list())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '[]')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date=dict(),
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(pub_date=dict())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '{}')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date=tuple(),
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(pub_date=tuple())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '()')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', pub_date=set(),
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(pub_date=set())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.pub_date, 'set()')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_order_without_pub_date(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1',
                                       image='000', divided='całe', tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_string_as_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image=' ', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, ' ')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status='1', image='\n ', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '\n ')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', pub_date='01.01.2020',
                                   order_status='1', image='\n ', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '\n ')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1238', pub_date='01.01.2020',
                                   order_status='1', image='image', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1238')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1238')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, 'image')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 5)

    def test_create_order_with_int_as_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image=1, divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '1')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image=0, divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '0')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status='1', image=-1, divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '-1')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

    def test_create_order_with_float_as_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image=1.1, divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '1.1')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image=-1.1, divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '-1.1')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_bool_as_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image=True, divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, 'True')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image=False, divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, 'False')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_none_as_image(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                       order_status='1', image=None, divided='całe',
                                       tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_structure_as_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image=list(), divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '[]')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image=dict(), divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '{}')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status='1', image=tuple(), divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '()')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', pub_date='01.01.2020',
                                   order_status='1', image=set(), divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, 'set()')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_order_without_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '?')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

    def test_create_order_with_string_as_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=' ',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, ' ')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='\n ',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '\n ')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='string',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'string')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_order_with_int_as_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=1,
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '1')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=0,
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '0')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=-1,
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '-1')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

    def test_create_order_with_float_as_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=1.1,
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '1.1')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=-1.1,
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '-1.1')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_bool_as_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=True,
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'True')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=False,
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'False')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_none_as_divided(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                       order_status='1', image='000', divided=None,
                                       tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_structure_as_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=list(),
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '[]')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=dict(),
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '{}')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=tuple(),
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '()')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', pub_date='01.01.2020',
                                   order_status='1', image='000', divided=set(),
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'set()')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_order_without_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '?')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

    def test_create_with_string_as_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number='')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=' ')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, ' ')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number='\n ')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '\n ')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number='number')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, 'number')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_with_int_as_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=1)
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '1')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=0)
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=-1)
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '-1')
        self.assertEqual(ActiveOrder.objects.count(), 3)

    def test_create_with_float_as_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=1.1)
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '1.1')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=-1.1)
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '-1.1')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_with_bool_as_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=True)
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, 'True')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=False)
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, 'False')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_with_none_as_tracking_number(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                       order_status='1', image='000', divided='całe', tracking_number=None)
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_with_structure_as_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=list())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '[]')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=dict())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '{}')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=tuple())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '()')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe', tracking_number=set())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, 'set()')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_without_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '?')
        self.assertEqual(ActiveOrder.objects.count(), 1)

    def test_create_with_string_as_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status=' ', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, ' ')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status='\n ', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '\n ')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', pub_date='01.01.2020',
                                   order_status='number', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, 'number')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_with_int_as_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status=1, image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status=0, image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '0')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status=-1, image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '-1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

    def test_create_with_float_as_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status=1.1, image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '1.1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status=-1.1, image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '-1.1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_with_bool_as_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status=True, image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, 'True')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status=False, image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, 'False')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_with_none_as_order_status(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                       order_status=None, image='000', divided='całe',
                                       tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_with_structure_as_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status=list(), image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '[]')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', pub_date='01.01.2020',
                                   order_status=dict(), image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '{}')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', pub_date='01.01.2020',
                                   order_status=tuple(), image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, '()')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', pub_date='01.01.2020',
                                   order_status=set(), image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, 'set()')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_without_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   image='000', divided='całe', tracking_number='0123456789012345678901')
        active_order.save()
        active_order =ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.pub_date, '01.01.2020')
        self.assertEqual(active_order.order_status, "('1', 'Nowe')")
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

    def test_create_without_arguments(self):
        with atomic():
            active_order = ActiveOrder()
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_str_method(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901')
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(str(active_order), 'QWERTYUIOP1234')

    def test_update_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   image='000', divided='całe', tracking_number='0123456789012345678901')
        active_order.save()
        self.assertTrue(active_order.update_status(ActiveOrder.order_statuses[1]))
        self.assertEqual(active_order.order_status, ('2', 'W przygotowaniu'))

        self.assertTrue(active_order.update_status(ActiveOrder.order_statuses[2]))
        self.assertEqual(active_order.order_status, ('3', 'Wysłane'))

        self.assertTrue(active_order.update_status(ActiveOrder.order_statuses[4]))
        self.assertEqual(active_order.order_status, ('5', 'Anulowane'))

        self.assertIsNone(active_order.update_status(ActiveOrder.order_statuses[3]))
        self.assertEqual(active_order.order_status, ('4', 'Zakończone'))
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_update_status_with_string_as_new_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   image='000', divided='całe', tracking_number='0123456789012345678901')
        active_order.save()
        self.assertFalse(active_order.update_status(''))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status(' '))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status('\n '))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status('new_status'))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status("('2', 'W przygotowaniu')"))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

    def test_update_status_with_int_as_new_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   image='000', divided='całe', tracking_number='0123456789012345678901')
        active_order.save()
        self.assertFalse(active_order.update_status(1))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status(0))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status(-1))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status(9999))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

    def test_update_status_with_float_as_new_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   image='000', divided='całe', tracking_number='0123456789012345678901')
        active_order.save()
        self.assertFalse(active_order.update_status(1.1))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status(-1.1))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

    def test_update_status_with_bool_as_new_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   image='000', divided='całe', tracking_number='0123456789012345678901')
        active_order.save()
        self.assertFalse(active_order.update_status(True))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status(False))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

    def test_update_status_with_none_as_new_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   image='000', divided='całe', tracking_number='0123456789012345678901')
        active_order.save()
        self.assertTrue(active_order.update_status(None))
        self.assertEqual(active_order.order_status, ('2', 'W przygotowaniu'))

    def test_update_status_with_structure_as_new_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   image='000', divided='całe', tracking_number='0123456789012345678901')
        active_order.save()
        self.assertFalse(active_order.update_status(list()))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status(dict()))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status(tuple()))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status(set()))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

    def test_update_status_without_new_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   image='000', divided='całe', tracking_number='0123456789012345678901')
        active_order.save()
        self.assertTrue(active_order.update_status())
        self.assertEqual(active_order.order_status, ('2', 'W przygotowaniu'))

        self.assertTrue(active_order.update_status())
        self.assertEqual(active_order.order_status, ('3', 'Wysłane'))

        self.assertIsNone(active_order.update_status())
        self.assertEqual(active_order.order_status, ('4', 'Zakończone'))
        self.assertEqual(ActiveOrder.objects.count(), 0)
        self.assertEqual(UnactiveOrder.objects.count(), 1)

    def test_complete_order(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', pub_date='01.01.2020',
                                   image='000', divided='całe', tracking_number='0123456789012345678901')
        active_order.save()
        active_order.complete_order()
        self.assertEqual(ActiveOrder.objects.count(), 0)
        self.assertEqual(UnactiveOrder.objects.count(), 1)
        unactive_order = UnactiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(unactive_order.order_number, active_order.order_number)
        self.assertEqual(unactive_order.pub_date, active_order.pub_date)
        self.assertEqual(unactive_order.image, active_order.image)
        self.assertEqual(unactive_order.owner, active_order.owner)
