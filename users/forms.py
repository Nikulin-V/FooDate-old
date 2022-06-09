from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """Form of user registration"""
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name'

    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return self.cleaned_data['password']


class UserChangeForm(forms.ModelForm):
    """Form of changing user information"""
    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'email'
