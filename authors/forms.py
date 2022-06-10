from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #add_placeholder(self.fields['username'], 'Your username')
        #add_placeholder(self.fields['email'], 'Your e-mail')
        #add_placeholder(self.fields['first_name'], 'Ex.: John')
        #add_placeholder(self.fields['last_name'], 'Ex.: Doe')

    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: John'
        }),
        label='First name',
        error_messages={
            'required': 'Write your first name',
        }
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex.: Doe'
        }),
        label='Last name',
        error_messages={
            'required': 'Write your last name',
        }
    )

    email = forms.CharField(
        help_text=(
            'E-mail must be valid.'),
        widget=forms.TextInput(attrs={
            'placeholder': 'Your e-mail'
        }),
        label='E-mail',
        error_messages={
            'required': 'Write your e-mail',
        }
    )

    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 20 characters.'
        ),
        widget=forms.TextInput(attrs={
            'placeholder': 'Your username'
        }),
        error_messages={
            'required': 'Write your username',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 20 characters',
        },
        min_length=4, max_length=20,
    )

    password = forms.CharField(
        required=True,
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }
        ),
        label='Password',
        validators=[strong_password],
        error_messages={
            'required': 'Write your password',
        })

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
        label='Re-password',
        error_messages={
            'required': 'Password and Re-password must be equal',
        }
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'This e-mail already in use.',
                code='invalid'
            )
        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and Re-password must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': password_confirmation_error,
            })
