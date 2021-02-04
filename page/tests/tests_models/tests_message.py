from django.test import TestCase
from django.db.utils import IntegrityError
from django.db.transaction import atomic
from django.contrib.auth.models import User, Group
from ...models import Message, MessagesThread


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
