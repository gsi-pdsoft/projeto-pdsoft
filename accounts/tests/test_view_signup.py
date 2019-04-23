from django.test import TestCase
from django.urls import resolve
from ..views import signup 
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from ..forms import SignUpForm
# Create your tests here.

class SignUpTests(TestCase):

	def setUp(self):
		url=reverse('signup')
		self.response = self.client.get(url)

	def test_signup_status_code(self):

		self.assertEquals(self.response.status_code,200)

	def test_signup_url_resolves_signup_view(self):
		view = resolve('/signup/')
		self.assertEquals(view.func, signup)

	def test_csrf(self):
		self.assertContains(self.response,'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, SignUpForm)


class SuccessfulSignUpTests(TestCase):

	def setUp(self):
		url = reverse('signup')
		data = {
			'first_name': 'Afonso',
			'last_name':'Santos',
			'username': 'Afonsinho',
			'email': 'a@test.com',
			'password1': 'abcdef12345',
			'password2': 'abcdef12345'
		}
		self.response = self.client.post(url, data)
		self.home_url = reverse('home')


		def test_user_redirection(self):
			self.assertRedirects(self.response, self.home_url)

		def test_user_authentication(self):

			response = self.client.get(self.home_url)
			user = response.context.get('user')
			self.assertTrue(user.is_authenticated)


		def test_form_input(self):
			self.assertContains(self.response, '<input', 7)
			self.assertContains(self.response, 'type="text"', 3)
			self.assertContains(self.response, 'type="email"', 1)
			self.assertContains(self.response, 'type="password"', 2)
