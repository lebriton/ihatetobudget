from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class IndexTestCase(TestCase):
    def setUp(self):
        self.credentials = credentials = dict(
            username="username", password="password"
        )
        User.objects.create_user(email="", **credentials)

    def test_view(self):
        client = Client()
        self.assertEqual(
            client.get(reverse("index"), follow=True).redirect_chain, []
        )
        client.login(**self.credentials)
        self.assertEqual(
            client.get(reverse("index"), follow=True).redirect_chain,
            [(reverse("sheets:index"), 302)],
        )
