from django.test import TestCase
from django.db.utils import IntegrityError
from django.db.transaction import atomic
import datetime
from .models import *


class ActiveOrderTestCase(TestCase):
    def setUp(self):
        names = ['z4l', 'besart', 'kasia', 'administracja', 'Pomoc techniczna', 'druk']
        for name in names:
            group = Group(name=name)
            group.save()
        self.groups = Group.objects.all()

    def test_create_order(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

    def test_create_order_with_string_as_owner(self):
        self.assertRaises(ValueError, ActiveOrder, owner='', order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=' ', order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner='\n ', order_number='QWERTYUIOP1234',  order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner='z4l', order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner='1', order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_int_as_owner(self):
        self.assertRaises(ValueError, ActiveOrder, owner=1, order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=0, order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=-1, order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_float_as_owner(self):
        self.assertRaises(ValueError, ActiveOrder, owner=1.1, order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=-1.1, order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_bool_as_owner(self):
        self.assertRaises(ValueError, ActiveOrder, owner=True, order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=False, order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_none_as_owner(self):
        with atomic():
            order = ActiveOrder(owner=None, order_number='QWERTYUIOP1234', order_status='1', image='000',
                                divided='całe', tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_structure_as_owner(self):
        self.assertRaises(ValueError, ActiveOrder, owner=list(), order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=dict(), order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=tuple(), order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

        self.assertRaises(ValueError, ActiveOrder, owner=set(), order_number='QWERTYUIOP1234', order_status='1',
                          image='000', divided='całe', tracking_number='0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_without_owner(self):
        with atomic():
            order = ActiveOrder(order_number='QWERTYUIOP1234', order_status='1', image='000', divided='całe',
                                tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_with_string_as_order_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='', order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number=' ', order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=' ')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, ' ')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='\n ', order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='\n ')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '\n ')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='Order number', order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='Order number')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'Order number')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

        active_order = ActiveOrder(owner=self.groups[0], order_number='Definitely too long order number',
                                   order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='Definitely too long order number')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'Definitely too long order number')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 5)

    def test_create_order_with_int_as_order_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number=1, order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=1)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '1')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number=0, order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=0)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '0')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number=-1, order_status='1', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=-1)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '-1')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

    def test_create_order_with_bool_as_order_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number=True, order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=True)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'True')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number=False, order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=False)
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'False')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_none_as_order_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number=None, order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901')
        self.assertRaises(IntegrityError, active_order.save)

    def test_create_order_with_structure_as_order_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number=list(), order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=list())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '[]')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number=dict(), order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=dict())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '{}')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number=tuple(), order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=tuple())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, '()')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number=set(), order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number=set())
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'set()')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_order_without_order_number(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], order_status='1', image='000', divided='całe',
                                       tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_string_as_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image=' ',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, ' ')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status='1', image='\n ',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '\n ')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', order_status='1', image='\n ',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '\n ')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1238', order_status='1', image='image',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1238')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1238')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, 'image')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 5)

    def test_create_order_with_int_as_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image=1,
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '1')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image=0,
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '0')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status='1', image=-1,
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '-1')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

    def test_create_order_with_float_as_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image=1.1,
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '1.1')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image=-1.1,
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '-1.1')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_bool_as_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image=True,
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, 'True')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image=False,
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, 'False')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_none_as_image(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1',
                                       image=None, divided='całe', tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_structure_as_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image=list(),
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '[]')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image=dict(),
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '{}')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status='1', image=tuple(),
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '()')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', order_status='1', image=set(),
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, 'set()')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_order_without_image(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '?')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

    def test_create_order_with_string_as_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided='', tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image='000',
                                   divided=' ', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, ' ')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status='1', image='000',
                                   divided='\n ', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '\n ')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', order_status='1', image='000',
                                   divided='string', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'string')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_order_with_int_as_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided=1, tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '1')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image='000',
                                   divided=0, tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '0')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status='1', image='000',
                                   divided=-1, tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '-1')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

    def test_create_order_with_float_as_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided=1.1, tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '1.1')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image='000',
                                   divided=-1.1, tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '-1.1')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_bool_as_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided=True, tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'True')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image='000',
                                   divided=False, tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'False')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_order_with_none_as_divided(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1',
                                       image='000', divided=None, tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_order_with_structure_as_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided=list(), tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '[]')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image='000',
                                   divided=dict(), tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '{}')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status='1', image='000',
                                   divided=tuple(), tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '()')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', order_status='1', image='000',
                                   divided=set(), tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'set()')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_order_without_divided(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, '?')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

    def test_create_with_string_as_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided='całe', tracking_number='', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image='000',
                                   divided='całe', tracking_number=' ', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, ' ')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status='1', image='000',
                                   divided='całe', tracking_number='\n ', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '\n ')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', order_status='1', image='000',
                                   divided='całe', tracking_number='number', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, 'number')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_with_int_as_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided='całe', tracking_number=1, pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '1')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image='000',
                                   divided='całe', tracking_number=0, pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status='1', image='000',
                                   divided='całe', tracking_number=-1, pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '-1')
        self.assertEqual(ActiveOrder.objects.count(), 3)

    def test_create_with_float_as_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided='całe', tracking_number=1.1, pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '1.1')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image='000',
                                   divided='całe', tracking_number=-1.1, pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '-1.1')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_with_bool_as_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided='całe', tracking_number=True, pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, 'True')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image='000',
                                   divided='całe', tracking_number=False, pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, 'False')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_with_none_as_tracking_number(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1',
                                       image='000', divided='całe', tracking_number=None)
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_with_structure_as_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided='całe', tracking_number=list(), pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '[]')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status='1', image='000',
                                   divided='całe', tracking_number=dict(), pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '{}')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status='1', image='000',
                                   divided='całe', tracking_number=tuple(), pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '()')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', order_status='1', image='000',
                                   divided='całe', tracking_number=set(), pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, 'set()')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_without_tracking_number(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided='całe', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '?')
        self.assertEqual(ActiveOrder.objects.count(), 1)

    def test_create_with_string_as_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status=' ', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, ' ')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status='\n ', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '\n ')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', order_status='number',
                                   image='000', divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.order_status, 'number')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_with_int_as_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status=1, image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status=0, image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '0')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status=-1, image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '-1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

    def test_create_with_float_as_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status=1.1, image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '1.1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status=-1.1, image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '-1.1')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_with_bool_as_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status=True, image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, 'True')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status=False, image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, 'False')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

    def test_create_with_none_as_order_status(self):
        with atomic():
            active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status=None,
                                       image='000', divided='całe', tracking_number='0123456789012345678901')
            self.assertRaises(IntegrityError, active_order.save)
        self.assertEqual(ActiveOrder.objects.count(), 0)

    def test_create_with_structure_as_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status=list(),
                                   image='000', divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
        self.assertEqual(active_order.order_status, '[]')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 1)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1235', order_status=dict(),
                                   image='000', divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1235')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1235')
        self.assertEqual(active_order.order_status, '{}')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 2)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1236', order_status=tuple(),
                                   image='000', divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1236')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1236')
        self.assertEqual(active_order.order_status, '()')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 3)

        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1237', order_status=set(), image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1237')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1237')
        self.assertEqual(active_order.order_status, 'set()')
        self.assertEqual(active_order.image, '000')
        self.assertEqual(active_order.divided, 'całe')
        self.assertEqual(active_order.tracking_number, '0123456789012345678901')
        self.assertEqual(ActiveOrder.objects.count(), 4)

    def test_create_without_order_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(active_order.owner.name, 'z4l')
        self.assertEqual(active_order.order_number, 'QWERTYUIOP1234')
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
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', order_status='1', image='000',
                                   divided='całe', tracking_number='0123456789012345678901',
                                   pub_date=datetime.date.today())
        active_order.save()
        active_order = ActiveOrder.objects.get(order_number='QWERTYUIOP1234')
        self.assertEqual(str(active_order), 'QWERTYUIOP1234')

    def test_update_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        self.assertTrue(active_order.update_status(ActiveOrder.order_statuses[1]))
        self.assertEqual(active_order.order_status, ('2', 'W przygotowaniu'))

        self.assertTrue(active_order.update_status(ActiveOrder.order_statuses[2]))
        self.assertEqual(active_order.order_status, ('3', 'Wysłane'))

        self.assertTrue(active_order.update_status(ActiveOrder.order_statuses[4]))
        self.assertEqual(active_order.order_status, ('5', 'Anulowane'))

        self.assertTrue(active_order.update_status(ActiveOrder.order_statuses[3]))
        self.assertEqual(active_order.order_status, ('4', 'Zakończone'))
        self.assertEqual(ActiveOrder.objects.count(), 1)

        self.assertIsNone(active_order.update_status(ActiveOrder.order_statuses[2]))
        self.assertEqual(active_order.order_status, ('4', 'Zakończone'))
        self.assertEqual(ActiveOrder.objects.count(), 1)

    def test_update_status_with_string_as_new_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
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
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
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
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        self.assertFalse(active_order.update_status(1.1))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status(-1.1))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

    def test_update_status_with_bool_as_new_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        self.assertFalse(active_order.update_status(True))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

        self.assertFalse(active_order.update_status(False))
        self.assertEqual(active_order.order_status, ('1', 'Nowe'))

    def test_update_status_with_none_as_new_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        self.assertTrue(active_order.update_status(None))
        self.assertEqual(active_order.order_status, ('2', 'W przygotowaniu'))

    def test_update_status_with_structure_as_new_status(self):
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
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
        active_order = ActiveOrder(owner=self.groups[0], order_number='QWERTYUIOP1234', image='000', divided='całe',
                                   tracking_number='0123456789012345678901', pub_date=datetime.date.today())
        active_order.save()
        self.assertTrue(active_order.update_status())
        self.assertEqual(active_order.order_status, ('2', 'W przygotowaniu'))

        self.assertTrue(active_order.update_status())
        self.assertEqual(active_order.order_status, ('3', 'Wysłane'))

        self.assertTrue(active_order.update_status())
        self.assertEqual(active_order.order_status, ('4', 'Zakończone'))
        self.assertEqual(ActiveOrder.objects.count(), 1)


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


class MessageThreadTestCase(TestCase):
    def setUp(self):
        names = ['z4l', 'besart', 'kasia', 'administracja', 'Pomoc techniczna', 'druk']
        for name in names:
            group = Group(name=name)
            group.save()
        self.groups = Group.objects.all()

    def test_create(self):
        thread = MessagesThread(subject='Subject')
        thread.save()
        thread.groups.set(self.groups[:3])
        thread = MessagesThread.objects.get(pk=thread.pk)
        for group in self.groups[:3]:
            self.assertIn(group, thread.groups.all())
        self.assertEqual(MessagesThread.objects.count(), 1)
        self.assertEqual(thread.subject, 'Subject')

    def test_create_with_string_as_subject(self):
        thread = MessagesThread(subject='')
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 1)
        self.assertEqual(thread.subject, '')

        thread = MessagesThread(subject=' ')
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 2)
        self.assertEqual(thread.subject, ' ')

        thread = MessagesThread(subject='\n ')
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 3)
        self.assertEqual(thread.subject, '\n ')

        thread = MessagesThread(subject='Subject')
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 4)
        self.assertEqual(thread.subject, 'Subject')

    def test_create_with_int_as_subject(self):
        thread = MessagesThread(subject=1)
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 1)
        self.assertEqual(thread.subject, '1')

        thread = MessagesThread(subject='0')
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 2)
        self.assertEqual(thread.subject, '0')

        thread = MessagesThread(subject=-1)
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 3)
        self.assertEqual(thread.subject, '-1')

    def test_create_with_float_as_subject(self):
        thread = MessagesThread(subject=1.1)
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 1)
        self.assertEqual(thread.subject, '1.1')

        thread = MessagesThread(subject=-1.1)
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 2)
        self.assertEqual(thread.subject, '-1.1')

    def test_create_with_bool_as_subject(self):
        thread = MessagesThread(subject=True)
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 1)
        self.assertEqual(thread.subject, 'True')

        thread = MessagesThread(subject=False)
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 2)
        self.assertEqual(thread.subject, 'False')

    def test_create_with_none_as_subject(self):
        with atomic():
            thread = MessagesThread(subject=None)
            self.assertRaises(IntegrityError, thread.save)
        self.assertEqual(MessagesThread.objects.count(), 0)

    def test_create_with_structure_as_subject(self):
        thread = MessagesThread(subject=list())
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 1)
        self.assertEqual(thread.subject, '[]')

        thread = MessagesThread(subject=dict())
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 2)
        self.assertEqual(thread.subject, '{}')

        thread = MessagesThread(subject=tuple())
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 3)
        self.assertEqual(thread.subject, '()')

        thread = MessagesThread(subject=set())
        thread.save()
        thread = MessagesThread.objects.get(pk=thread.pk)
        self.assertEqual(MessagesThread.objects.count(), 4)
        self.assertEqual(thread.subject, 'set()')

    def test_str_method(self):
        thread = MessagesThread(subject='Subject')
        thread.save()
        self.assertEqual(MessagesThread.objects.count(), 1)
        self.assertEqual(str(thread), thread.subject)

    def test_delete_method(self):
        user = User(username='User')
        user.save()
        thread = MessagesThread(subject='Subject')
        thread.save()
        message = Message(thread=thread, message_op=user, message_text='Text')
        message.save()
        self.assertEqual(MessagesThread.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 1)
        thread.delete_thread()
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 1)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 0)
        self.assertEqual(Message.objects.filter(archive=True).count(), 1)
        self.assertEqual(Message.objects.filter(archive=False).count(), 0)


class MessageTestCase(TestCase):
    def setUp(self):
        self.user = User(username='User')
        self.user.save()
        self.thread = MessagesThread(subject='Subject')
        self.thread.save()
        group = Group(name='group')
        group.save()
        self.user.groups.add(group)
        self.thread.groups.add(group)

    def test_create(self):
        message = Message(thread=self.thread, message_op=self.user, message_text='Text')
        message.save()
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, 'Text')

    def test_create_with_string_as_thread(self):
        self.assertRaises(ValueError, Message, thread='', message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=' ', message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread='\n ', message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread='Subject', message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread='1', message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_int_as_thread(self):
        self.assertRaises(ValueError, Message, thread=1, message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=0, message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=-1, message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_float_as_thread(self):
        self.assertRaises(ValueError, Message, thread=1.1, message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=-1.1, message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_bool_as_thread(self):
        self.assertRaises(ValueError, Message, thread=True, message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=False, message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_none_as_thread(self):
        with atomic():
            message = Message(thread=None, message_op=self.user, message_text='Text')
            self.assertRaises(IntegrityError, message.save)
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_structure_as_thread(self):
        self.assertRaises(ValueError, Message, thread=list(), message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=dict(), message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=tuple(), message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=set(), message_op=self.user, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

    def test_create_without_thread(self):
        with atomic():
            message = Message(message_op=self.user, message_text='Text')
            self.assertRaises(IntegrityError, message.save)
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_string_as_message_op(self):
        self.assertRaises(ValueError, Message, thread=self.thread, message_op='', message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=self.thread, message_op=' ', message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=self.thread, message_op='\n ', message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=self.thread, message_op='User', message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=self.thread, message_op='1', message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_int_as_message_op(self):
        self.assertRaises(ValueError, Message, thread=self.thread, message_op=1, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=self.thread, message_op=0, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=self.thread, message_op=-1, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_float_as_message_op(self):
        self.assertRaises(ValueError, Message, thread=self.thread, message_op=1.1, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=self.thread, message_op=-1.1, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_bool_as_message_op(self):
        self.assertRaises(ValueError, Message, thread=self.thread, message_op=True, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=self.thread, message_op=False, message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_none_as_message_op(self):
        with atomic():
            message = Message(thread=self.thread, message_op=None, message_text='Text')
            self.assertRaises(IntegrityError, message.save)
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_structure_as_message_op(self):
        self.assertRaises(ValueError, Message, thread=self.thread, message_op=list(), message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=self.thread, message_op=dict(), message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=self.thread, message_op=tuple(), message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

        self.assertRaises(ValueError, Message, thread=self.thread, message_op=set(), message_text='Text')
        self.assertEqual(Message.objects.count(), 0)

    def test_create_without_message_op(self):
        with atomic():
            message = Message(thread=self.thread, message_text='Text')
            self.assertRaises(IntegrityError, message.save)
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_string_as_message_text(self):
        message = Message(thread=self.thread, message_op=self.user, message_text='')
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, '')

        message = Message(thread=self.thread, message_op=self.user, message_text=' ')
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, ' ')

        message = Message(thread=self.thread, message_op=self.user, message_text='\n ')
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 3)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, '\n ')

        message = Message(thread=self.thread, message_op=self.user, message_text='Text')
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 4)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, 'Text')

        message = Message(thread=self.thread, message_op=self.user, message_text='1')
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 5)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, '1')

    def test_create_with_int_as_message_text(self):
        message = Message(thread=self.thread, message_op=self.user, message_text=1)
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, '1')

        message = Message(thread=self.thread, message_op=self.user, message_text=0)
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, '0')

        message = Message(thread=self.thread, message_op=self.user, message_text=-1)
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 3)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, '-1')

    def test_create_with_float_as_message_text(self):
        message = Message(thread=self.thread, message_op=self.user, message_text=1.1)
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, '1.1')

        message = Message(thread=self.thread, message_op=self.user, message_text=-1.1)
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, '-1.1')

    def test_create_with_bool_as_message_text(self):
        message = Message(thread=self.thread, message_op=self.user, message_text=True)
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, 'True')

        message = Message(thread=self.thread, message_op=self.user, message_text=False)
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, 'False')

    def test_create_with_none_as_message_text(self):
        with atomic():
            message = Message(thread=self.thread, message_op=self.user, message_text=None)
            self.assertRaises(IntegrityError, message.save)
        self.assertEqual(Message.objects.count(), 0)

    def test_create_with_structure_as_message_text(self):
        message = Message(thread=self.thread, message_op=self.user, message_text=list())
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, '[]')

        message = Message(thread=self.thread, message_op=self.user, message_text=dict())
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, '{}')

        message = Message(thread=self.thread, message_op=self.user, message_text=tuple())
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 3)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, '()')

        message = Message(thread=self.thread, message_op=self.user, message_text=set())
        message.save()
        message = Message.objects.get(pk=message.pk)
        self.assertEqual(Message.objects.count(), 4)
        self.assertEqual(message.thread, self.thread)
        self.assertEqual(message.message_op, self.user)
        self.assertEqual(message.message_text, 'set()')

    def test_create_without_message_text(self):
        with atomic():
            message = Message(thread=self.thread, message_op=self.user)
            self.assertRaises(IntegrityError, message.save)
        self.assertEqual(Message.objects.count(), 0)

    def test_str_method(self):
        message = Message(thread=self.thread, message_op=self.user, message_text='Text')
        message.save()
        self.assertEqual(str(message), 'Subject')

    def test_delete_message(self):
        message = Message(thread=self.thread, message_op=self.user, message_text='Text')
        message.save()
        self.assertEqual(Message.objects.count(), 1)
        message.delete_message()
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 1)
        self.assertEqual(Message.objects.filter(archive=False).count(), 0)


class NotificationTestCase(TestCase):
    def setUp(self):
        self.user = User(username='User')
        self.user.save()
        self.thread = MessagesThread(subject='Subject')
        self.thread.save()
        self.group = Group(name='group')
        self.group.save()
        self.user.groups.add(self.group)
        self.thread.groups.add(self.group)

    def test_add_notification(self):
        notification = Notification.add_notification(self.user, self.thread)
        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.thread, self.thread)
        self.assertEqual(Notification.objects.count(), 1)

        notification = Notification.add_notification(self.user, self.thread)
        self.assertIsInstance(notification, Notification)
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.thread, self.thread)
        self.assertEqual(Notification.objects.count(), 1)

    def test_add_notification_when_user_not_in_thread_groups(self):
        self.thread.groups.remove(self.group)
        self.assertIsNone(Notification.add_notification(self.user, self.thread))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_string_as_user(self):
        self.assertIsNone(Notification.add_notification('', self.thread))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(' ', self.thread))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification('\n ', self.thread))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification('User', self.thread))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification('1', self.thread))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_int_as_user(self):
        self.assertIsNone(Notification.add_notification(1, self.thread))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(0, self.thread))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(-1, self.thread))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_float_as_user(self):
        self.assertIsNone(Notification.add_notification(1.1, self.thread))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(-1.1, self.thread))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_bool_as_user(self):
        self.assertIsNone(Notification.add_notification(True, self.thread))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(False, self.thread))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_none_as_user(self):
        self.assertIsNone(Notification.add_notification(None, self.thread))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_structure_as_user(self):
        self.assertIsNone(Notification.add_notification(list(), self.thread))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(dict(), self.thread))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(tuple(), self.thread))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(set(), self.thread))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_without_user(self):
        self.assertRaises(TypeError, Notification.add_notification, thread=self.thread)
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_string_as_thread(self):
        self.assertIsNone(Notification.add_notification(self.user, ''))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(self.user, ' '))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(self.user, '\n '))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(self.user, 'Subject'))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(self.user, '1'))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_int_as_thread(self):
        self.assertIsNone(Notification.add_notification(self.user, 1))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(self.user, 0))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(self.user, -1))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_float_as_thread(self):
        self.assertIsNone(Notification.add_notification(self.user, 1.1))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(self.user, -1.1))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_bool_as_thread(self):
        self.assertIsNone(Notification.add_notification(self.user, True))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(self.user, False))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_none_as_thread(self):
        self.assertIsNone(Notification.add_notification(self.user, None))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_with_structure_as_thread(self):
        self.assertIsNone(Notification.add_notification(self.user, list()))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(self.user, dict()))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(self.user, tuple()))
        self.assertEqual(Notification.objects.count(), 0)

        self.assertIsNone(Notification.add_notification(self.user, set()))
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_without_thread(self):
        self.assertRaises(TypeError, Notification.add_notification, user=self.user)
        self.assertEqual(Notification.objects.count(), 0)

    def test_add_notification_without_arguments(self):
        self.assertRaises(TypeError, Notification.add_notification)
        self.assertEqual(Notification.objects.count(), 0)

    def test_str_method(self):
        notification = Notification.add_notification(self.user, self.thread)
        self.assertIsInstance(notification, Notification)
        self.assertEqual(str(notification), self.thread.subject)
