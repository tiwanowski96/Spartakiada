from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email',
                  'password1', 'password2']


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
            cleaned_data = super(UserLoginForm, self).clean()
            user = authenticate(
                username=cleaned_data['username'],
                password=cleaned_data['password'],
            )

            if user is None:
                raise forms.ValidationError(
                    'Nieprawidłowy login lub hasło'
                )
            cleaned_data['user'] = user
            return cleaned_data

