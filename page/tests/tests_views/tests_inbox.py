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

    def test_with_authentication_without_groups(self):
        self.user.groups.remove(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.get('/inbox/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

    def test_with_authentication_as_wrong_group(self):
        self.user.groups.remove(self.groups['administracja'])
        self.client.force_login(self.user)
        response = self.client.get('/inbox/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

        self.user.groups.remove(self.groups['4dich'])
        self.user.groups.add(self.groups['besart'])
        self.client.force_login(self.user)
        response = self.client.get('/inbox/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

        self.user.groups.remove(self.groups['besart'])
        self.user.groups.add(self.groups['kasia'])
        self.client.force_login(self.user)
        response = self.client.get('/inbox/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

        self.user.groups.remove(self.groups['kasia'])
        self.user.groups.add(self.groups['Pomoc techniczna'])
        self.client.force_login(self.user)
        response = self.client.get('/inbox/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

        self.user.groups.remove(self.groups['Pomoc techniczna'])
        self.user.groups.add(self.groups['administracja'])
        self.client.force_login(self.user)
        response = self.client.get('/inbox/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

    def test_with_authentication_as_proper_group(self):
        self.client.force_login(self.user)
        response = self.client.get('/inbox/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.templates[0].name, 'page/admin_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertIn(self.thread, response.context[0].dicts[3]['message_threads'])
        self.assertIn(self.notification.thread.pk, response.context[0].dicts[3]['notifications'])

        self.notification.delete()
        self.user.groups.remove(self.groups['administracja'], self.groups['4dich'])
        self.user.groups.add(self.groups['druk'])
        self.client.force_login(self.user)
        response = self.client.get('/inbox/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/inbox/')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.templates[0].name, 'page/user_inbox.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.context[0].dicts[3]['message_threads']), 0)
        self.assertEqual(len(response.context[0].dicts[3]['notifications']), 0)

    def test_post_method(self):
        self.user.groups.add(self.groups['administracja'], self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.post('/inbox/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/orders/1/a/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/orders/1/a/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/admin_orders.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
