from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username', max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter unique username',
            'autocomplete': 'off'
        }))
    password = forms.CharField(
        label='Password', max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '**********'
            }))


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label='Username', max_length=300,
        validators=[RegexValidator(
            r'^[0-9a-zA-Z_]*$')],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Create that unique username you love',
                'autocomplete': 'off'
            }))
    password = forms.CharField(
        label='Password', max_length=100,
        widget=forms.PasswordInput(
            attrs={
              'placeholder': 'Create secret password'
            }))
    verify_password = forms.CharField(
        label='Verify Password', max_length=100,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Verify secret password'
        }))

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("This username has been used")

    def clean(self):
        try:
            if self.cleaned_data['password'] != self.cleaned_data['verify_password']:
                raise forms.ValidationError("Passwords do not match")
        except KeyError:
            return self.cleaned_data

    def save(self):
        new_user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        return new_user
