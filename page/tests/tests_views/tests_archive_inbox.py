from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from ...models import MessagesThread


class ArchiveInboxTestCase(TestCase):
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
        self.thread.groups.add(self.groups['4dich'])

    def test_without_authentication(self):
        response = self.client.get('/archive/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/archive/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

    def test_with_authentication_without_group(self):
        self.client.force_login(self.user)
        response = self.client.get('/archive/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

    def test_with_authentication_as_wrong_group(self):
        self.user.groups.add(self.groups['administracja'])
        self.client.force_login(self.user)
        response = self.client.get('/archive/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')

        self.user.groups.remove(self.groups['administracja'])
        self.user.groups.add(self.groups['4dich'])
        self.client.force_login(self.user)
        response = self.client.get('/archive/', follow=True)
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
        response = self.client.get('/archive/', follow=True)
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
        response = self.client.get('/archive/', follow=True)
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
        response = self.client.get('/archive/', follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 2)
        self.assertEqual(response.redirect_chain[0][0], '/o/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.redirect_chain[1][0], '/')
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
