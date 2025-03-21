from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=254)  # Mudei de 'usuario' para 'username'
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError('O nome de usuário é obrigatório.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Usuário ou senha inválidos.')

        return cleaned_data

    
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', max_length=254)
    first_name = forms.CharField(label='Nome', max_length=30)
    last_name = forms.CharField(label='Sobrenome', max_length=150)
    cpf = forms.CharField(label='CPF', max_length=11)
    phone = forms.CharField(label='Telefone', max_length=11)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'cpf', 'phone', 'password1', 'password2']

    def clean_repeat_password(self):
        password = self.cleaned_data.get('password1')
        repeat_password = self.cleaned_data.get('repeat_password')

        if password != repeat_password:
            raise ValidationError('As senhas não coincidem.')

        return repeat_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  # Define a senha de forma segura
        if commit:
            user.save()
        return user


    