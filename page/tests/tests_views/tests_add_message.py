from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from ...models import MessagesThread, Message, Notification


class AddMessageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(username='User', password='password')
        self.user.save()
        names = ['administracja', 'druk', '4dich', 'besart', 'kasia', 'Pomoc techniczna']
        self.groups = {name: Group(name=name) for name in names}
        for group in self.groups.values():
            group.save()

    def test_without_authentication(self):
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/message/add/subject/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

    def test_with_authentication_without_group(self):
        self.client.force_login(self.user)
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 3)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/o/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[2][0], '/')
        self.assertEqual(response.redirect_chain[2][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessagesThread.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)

    def test_with_authentication_as_only_administracja_group(self):
        self.user.groups.add(self.groups['administracja'])
        self.client.force_login(self.user)
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 3)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/o/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[2][0], '/')
        self.assertEqual(response.redirect_chain[2][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessagesThread.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)

    def test_with_authentication_as_wrong_group(self):
        self.user.groups.add(self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 3)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/o/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[2][0], '/')
        self.assertEqual(response.redirect_chain[2][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessagesThread.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)

        self.user.groups.remove(self.groups['4dich'])
        self.user.groups.add(self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 3)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/o/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[2][0], '/')
        self.assertEqual(response.redirect_chain[2][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessagesThread.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)

        self.user.groups.remove(self.groups['besart'])
        self.user.groups.add(self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 3)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/o/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[2][0], '/')
        self.assertEqual(response.redirect_chain[2][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessagesThread.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)

        self.user.groups.remove(self.groups['kasia'])
        self.user.groups.add(self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 3)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/o/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[2][0], '/')
        self.assertEqual(response.redirect_chain[2][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessagesThread.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)

        self.user.groups.add(self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 3)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/o/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[2][0], '/')
        self.assertEqual(response.redirect_chain[2][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(MessagesThread.objects.count(), 0)
        self.assertEqual(Notification.objects.count(), 0)

    def test_with_authentication_with_proper_group(self):
        second_user = User(username='Second User', password='password')
        second_user.save()
        second_user.groups.add(self.groups['druk'])

        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(MessagesThread.objects.count(), 1)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['4dich'])
        self.user.groups.add(self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(MessagesThread.objects.count(), 2)
        self.assertEqual(Notification.objects.count(), 2)

        self.client.force_login(self.user)
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(Message.objects.count(), 3)
        self.assertEqual(MessagesThread.objects.count(), 2)
        self.assertEqual(Notification.objects.count(), 2)

        self.client.force_login(second_user)
        response = self.client.post('/message/add/subject/', {'message_text': 'text'}, follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/user_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(Message.objects.count(), 4)
        self.assertEqual(MessagesThread.objects.count(), 3)
        self.assertEqual(Notification.objects.count(), 2)
