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

    def test_with_authentication_without_group(self):
        self.client.force_login(self.user)
        response = self.client.get('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 3)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/o/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[2][0], '/')
        self.assertEqual(response.redirect_chain[2][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

    def test_with_authentication_as_wrong_group(self):
        self.user.groups.add(self.groups['administracja'])
        self.client.force_login(self.user)
        response = self.client.get('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 3)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/o/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[2][0], '/')
        self.assertEqual(response.redirect_chain[2][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

        self.user.groups.add(self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.get('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/orders/1/a/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_orders.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

        self.user.groups.remove(self.groups['besart'])
        self.user.groups.add(self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.get('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/orders/1/a/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_orders.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

        self.user.groups.remove(self.groups['kasia'])
        self.user.groups.add(self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.get('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/orders/1/a/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_orders.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

    def test_with_authentication_as_proper_group(self):
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.get('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/archive/1/1')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.templates[0].name, 'page/archive_thread.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(response.context[1].dicts[3]['notification'], 0)
        self.assertEqual(len(response.context[1].dicts[3]['messages_thread']), 10)
        self.assertEqual(response.context[1].dicts[3]['next_page'], 2)
        self.assertEqual(response.context[1].dicts[3]['prev_page'], 0)

        self.client.force_login(self.user)
        response = self.client.get('/archive/1/2', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/archive/1/2')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.templates[0].name, 'page/archive_thread.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(response.context[1].dicts[3]['notification'], 0)
        self.assertEqual(len(response.context[1].dicts[3]['messages_thread']), 1)
        self.assertEqual(response.context[1].dicts[3]['next_page'], 0)
        self.assertEqual(response.context[1].dicts[3]['prev_page'], 1)

        self.user.groups.remove(self.groups['druk'])
        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.get('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/archive/1/1')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.templates[0].name, 'page/archive_thread.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(response.context[1].dicts[3]['notification'], 0)
        self.assertEqual(len(response.context[1].dicts[3]['messages_thread']), 10)
        self.assertEqual(response.context[1].dicts[3]['next_page'], 2)
        self.assertEqual(response.context[1].dicts[3]['prev_page'], 0)

        self.client.force_login(self.user)
        response = self.client.get('/archive/1/2', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/archive/1/2')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.templates[0].name, 'page/archive_thread.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(response.context[1].dicts[3]['notification'], 0)
        self.assertEqual(len(response.context[1].dicts[3]['messages_thread']), 1)
        self.assertEqual(response.context[1].dicts[3]['next_page'], 0)
        self.assertEqual(response.context[1].dicts[3]['prev_page'], 1)

    def test_without_messages(self):
        for message in Message.objects.filter(thread=self.thread):
            message.delete()
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.get('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/archive/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/archive/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/archive_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

    def test_post_method(self):
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.post('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/archive/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/archive/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/archive_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

    def test_put_method(self):
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.put('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/archive/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/archive/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/archive_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

    def test_delete_method(self):
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.delete('/archive/1/1', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/archive/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/archive/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/archive_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
