from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from ..models import Board, Topic, Post

class LoginRequiredNewTopicTests(TestCase):
	def setUp(self):
		Board.objects.create(name='Django', description='Django board.')
		self.url = reverse('new_topic', kwargs={'pk': 1})
		self.response = self.client.get(self.url)

	def test_redirection(self):
		login_url = reverse('login')
		self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))