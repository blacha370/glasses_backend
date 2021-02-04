from django.test import TestCase, Client
from django.contrib.auth.models import User, Group


class IndexTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(username='User', password='password')
        admin_group = Group(name='administracja')
        admin_group.save()
        user_group = Group(name='druk')
        user_group.save()
        self.groups = {'administracja': admin_group, 'druk': user_group}

    def test_index_without_authenticate(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.request['PATH_INFO'], '/')
