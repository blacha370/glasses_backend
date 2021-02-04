from django.test import TestCase
from django.db.utils import IntegrityError
from django.db.transaction import atomic
from django.contrib.auth.models import Group, User
from ...models import MessagesThread, Message


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
