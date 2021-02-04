from django.test import TestCase
from ...models import *


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
