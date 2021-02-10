from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from ...models import Message, MessagesThread, Notification


class AddNewMessageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(username='User', password='password')
        self.user.save()
        names = ['administracja', 'druk', '4dich', 'besart', 'kasia', 'Pomoc techniczna']
        self.groups = {name: Group(name=name) for name in names}
        for group in self.groups.values():
            group.save()

    def test_without_authentication(self):
        response = self.client.post('/message/add_new/', {'reciever': 'besart',
                                                          'message_subject': 'subject', 'message_text': 'text'},
                                    follow=True)
        self.assertEqual(response.request['PATH_INFO'], '/')
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], '/?next=/message/add_new/')
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.templates[0].name, 'page/index.html')
        self.assertEqual(response.templates[1].name, 'page/base.html')
