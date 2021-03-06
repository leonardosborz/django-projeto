
from unittest import TestCase

from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('email', 'Your e-mail'),
        ('username', 'Your username'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('username', 'Username'),
        ('password', 'Password'),
        ('password2', 'Re-password'),
    ])
    def test_fields_label_is_correct(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(current_label, label)

    @parameterized.expand([
        ('email', 'E-mail must be valid.'),
        ('username', (
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 20 characters.'
        )),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.')),
    ])
    def test_fields_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        current_help_text = form[field].help_text
        self.assertEqual(current_help_text, help_text)


class AuthorRegisterFormIntegratedTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'StrongPassword1',
            'password2': 'StrongPassword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Write your username'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('email', 'Write your e-mail'),
        ('password', 'Write your password'),
        ('password2', 'Password and Re-password must be equal'),

    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'jon'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have at least 4 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        #self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_lower_than_20(self):
        self.form_data['username'] = 'jonhdooooooooooooooooooe'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Username must have less than 20 characters'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_and_password_confirmation_are_iqual(self):
        self.form_data['password'] = 'Abcd1234'
        self.form_data['password2'] = 'Abcd123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password and Re-password must be equal'

        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = 'Abcd1234'
        self.form_data['password2'] = 'Abcd1234'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_password_field_is_strong(self):
        self.form_data['password'] = 'Abcd'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Invalid password.'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_send_get_to_registration_create_view_return_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')

        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'This e-mail already in use.'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('authors:register_create')

        self.form_data.update({
            'username': 'testeuser',
            'password': 'Abc12345',
            'password2': 'Abc12345',
        })

        response = self.client.post(url, data=self.form_data, follow=True)

        is_autenticated = self.client.login(
            username='testeuser',
            password='Abc12345'
        )
        self.assertTrue(is_autenticated)
