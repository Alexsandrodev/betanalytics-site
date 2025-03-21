from django.shortcuts import render, redirect
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from .forms import LoginForm, RegisterForm

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']    

            print(username, password)  # Debug para verificar os dados

            user = authenticate(request, username=username, password=password)

            print(user)  # Verifique se retorna um usuário válido

            if user is not None:
                login(request, user)  # Faz o login do usuário
                messages.success(request, 'Login bem-sucedido!')
                return redirect('home')  # Redireciona após login
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
    
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})





def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.full_name = f"{user.first_name} {user.last_name}".strip()
            user.is_active = True
            user.subscribed_plan = None
            user.save()

            # Mensagem de sucesso
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('login')
        else:
            print('invalid registration details')

    return render(request, "registration/register.html", {"form": form})


def forgot_Password_view(request):
    pass


def loggout_view(request):
    if request.user.is_authenticated and request.session.session_key:
        try:
            # Exclui a sessão do banco de dados
            Session.objects.get(session_key=request.session.session_key).delete()
        except Session.DoesNotExist:
            pass
        
    logout(request)
    return redirect('login')