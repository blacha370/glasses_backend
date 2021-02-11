from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from ...models import Message, MessagesThread, Notification


class DeleteMessageThreadTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(username='User', password='password')
        self.user.save()
        names = ['administracja', 'druk', '4dich', 'besart', 'kasia', 'Pomoc techniczna']
        self.groups = {name: Group(name=name) for name in names}
        for group in self.groups.values():
            group.save()
        self.thread = MessagesThread(subject='subject')
        self.thread.save()
        self.thread.groups.add(self.groups['4dich'], self.groups['druk'])
        for i in range(5):
            message = Message(thread=self.thread, message_op=self.user, message_text='Message #{}'.format(i))
            message.save()
        notification = Notification(user=self.user, thread=self.thread)
        notification.save()

    def test_without_authentication(self):
        response = self.client.get('/message/delete/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/message/delete/1')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)
