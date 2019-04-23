from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.urls import resolve
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import views as auth_views
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class PasswordResetDoneTests(TestCase):
	def setUp(self):
		url = reverse('password_reset_done')
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)

	def test_view_function(self):
		view = resolve('/reset/done/')
		self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)


class PasswordResetConfirmTests(TestCase):
	def setUp(self):
		user = User.objects.create_user(first_name='afonso', last_name='silva', username='zé', email='as@a.pt', password='testing123')
		self.uid=urlsafe_base64_encode(force_bytes(user.pk)).decode()
		self.token = default_token_generator.make_token(user)

		url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
		self.response = self.client.get(url, follow=True)

	def test_status_code(self):
		self.assertEquals(self.response.status_code, 200)
		
	def test_view_function(self):
		view = resolve('/reset/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
		self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)

	def test_csrf(self):
		self.assertContains(self.response, 'csrfmiddlewaretoken')

	def test_contains_form(self):
		form = self.response.context.get('form')
		self.assertIsInstance(form, SetPasswordForm)

	def test_form_inputs(self):
		self.assertContains(self.response, '<input', 3)
		self.assertContains(self.response, 'type="password"', 2)

class InvalidPasswordResetConfirmTest(TestCase):
	"""docstring for InvalidPasswordResetConfirmTest"""
	def setUp(self):
		user = User.objects.create_user(first_name='afonsinho', last_name='silva', username='zezinho', email='ze@a.pt', password='testing123')
		self.uid=urlsafe_base64_encode(force_bytes(user.pk)).decode()
		self.token = default_token_generator.make_token(user)

		user.set_password('abcdef123')
		user.save()

		url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
		self.response = self.client.get(url)



	def test_status_code(self):
		self.assertEquals(self.response.status_code,200)

	def test_html(self):
		password_reset_url = reverse('password_reset')
		self.assertContains(self.response, 'invalid password reset link')
		self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))


class PasswordResetCompleteTests(TestCase):

	def setUp(self):
		url = reverse('password_reset_complete')
		self.response = self.client.get(url)

	def test_status_code(self):
		self.assertEquals(self.response.status_code,200)

	def test_view_function(self):
		view = resolve('/reset/complete/')
		self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)