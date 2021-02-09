from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from ...models import Notification, MessagesThread


class InboxTestCase(TestCase):
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
        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.thread = MessagesThread(subject='Thread subject')
        self.thread.save()
        self.thread.groups.add(self.groups['4dich'])
        self.notification = Notification(user=self.user, thread=self.thread)
        self.notification.save()

    def test_without_authentication(self):
        response = self.client.get('/inbox/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

