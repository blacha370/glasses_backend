from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from ...models import MessagesThread, Message, Notification


class ArchiveThreadTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(username='User', password='password')
        self.user.save()
        names = ['administracja', 'druk', '4dich', 'besart', 'kasia', 'Pomoc techniczna']
        self.groups = {}
        for name in names:
            group = Group(name=name)
            group.save()
            self.groups[name] = group
        self.thread = MessagesThread(subject='subject', archive=True)
        self.thread.save()
        self.thread.groups.add(self.groups['4dich'], self.groups['druk'])
        for i in range(11):
            message = Message(thread=self.thread, message_op=self.user, message_text='Message #{}'.format(i),
                              archive=True)
            message.save()
        notification = Notification(user=self.user, thread=self.thread)
        notification.save()

    def test_without_authentication(self):
        response = self.client.get('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/archive/1/1')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
