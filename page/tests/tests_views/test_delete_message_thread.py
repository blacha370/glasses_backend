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

    def test_with_authentication_without_group(self):
        self.client.force_login(self.user)
        response = self.client.get('/message/delete/1', follow=True)
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
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

    def test_with_authentication_with_wrong_group(self):
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.get('/message/delete/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/user_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['druk'])
        self.user.groups.add(self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.get('/message/delete/1', follow=True)
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
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['4dich'])
        self.user.groups.add(self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.get('/message/delete/1', follow=True)
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
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['besart'])
        self.user.groups.add(self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.get('/message/delete/1', follow=True)
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
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['kasia'])
        self.user.groups.add(self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.get('/message/delete/1', follow=True)
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
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

    def test_with_authentication_with_wrong_administracja_group(self):
        self.user.groups.add(self.groups['administracja'], self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.get('/message/delete/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['besart'])
        self.user.groups.add(self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.get('/message/delete/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['kasia'])
        self.user.groups.add(self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.get('/message/delete/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

    def test_with_authentication_as_proper_group(self):
        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.get('/message/delete/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 1)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 0)
        self.assertEqual(Message.objects.filter(archive=True).count(), 5)
        self.assertEqual(Message.objects.filter(archive=False).count(), 0)
        self.assertEqual(Notification.objects.count(), 0)

    def test_delete_not_existing_message(self):
        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.get('/message/delete/2', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

    def test_post_method_without_authentication(self):
        response = self.client.post('/message/delete/1', follow=True)
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

    def test_post_method_with_authentication_without_group(self):
        self.client.force_login(self.user)
        response = self.client.post('/message/delete/1', follow=True)
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
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

    def test_post_method_with_authentication_with_wrong_group(self):
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.post('/message/delete/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/user_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['druk'])
        self.user.groups.add(self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.post('/message/delete/1', follow=True)
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
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['4dich'])
        self.user.groups.add(self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.post('/message/delete/1', follow=True)
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
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['besart'])
        self.user.groups.add(self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.post('/message/delete/1', follow=True)
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
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['kasia'])
        self.user.groups.add(self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.post('/message/delete/1', follow=True)
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
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

    def test_post_method_with_authentication_with_wrong_administracja_group(self):
        self.user.groups.add(self.groups['administracja'], self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.post('/message/delete/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['besart'])
        self.user.groups.add(self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.post('/message/delete/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

        self.user.groups.remove(self.groups['kasia'])
        self.user.groups.add(self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.post('/message/delete/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)

    def test_post_method_with_authentication_as_proper_group(self):
        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.post('/message/delete/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/inbox/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(MessagesThread.objects.filter(archive=True).count(), 0)
        self.assertEqual(MessagesThread.objects.filter(archive=False).count(), 1)
        self.assertEqual(Message.objects.filter(archive=True).count(), 0)
        self.assertEqual(Message.objects.filter(archive=False).count(), 5)
        self.assertEqual(Notification.objects.count(), 1)
