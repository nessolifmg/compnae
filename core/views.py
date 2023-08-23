from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import transaction
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from .forms import UserCreationForm, FornecedorForm

ROLE_SERVIDOR = 'servidor'
ROLE_FORNECEDOR = 'fornecedor'
def redirect_based_on_role(user):
    """
    Realiza o redirecionamento com base nas roles do usuário.
    """
    if has_role(user, ROLE_SERVIDOR):
        return redirect('/servidor')
    elif has_role(user, ROLE_FORNECEDOR):
        return redirect('/fornecedor')
    else:
        return redirect('pagina-padrao')

def login_user(request):
    if request.method == "POST":
        form_login = AuthenticationForm(request, data=request.POST)
        if form_login.is_valid():
            username = form_login.cleaned_data.get('username')
            password = form_login.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Verificar as permissões ou grupo do usuário e redirecionar adequadamente
                return redirect_based_on_role(user)
            else:
                messages.error(request, "Usuário ou senha inválidos!")
    else:
        form_login = AuthenticationForm()
    context = {
        'form_login': form_login
    }
    return render(request, 'login.html', context=context)


# Função de logout do sistema
@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('/')


# Função para realizar o cadastro de fornecedores
def register_supplier(request):
    if request.method == "POST":
        form_user = UserCreationForm(request.POST)
        form_fornecedor = FornecedorForm(request.POST)
        if form_user.is_valid() and form_fornecedor.is_valid():
            with transaction.atomic():
                user = form_user.save()
                assign_role(user, 'fornecedor')
                fornecedor = form_fornecedor.save(commit=False)
                fornecedor.user = user
                fornecedor.save()
            messages.success(request, "Fornecedor cadastrado com sucesso!")
            return redirect('/')
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form_user = UserCreationForm()
        form_fornecedor = FornecedorForm()
    context = {
        'form_usuario': form_user,
        'form_fornecedor': form_fornecedor
    }
    return render(request, 'cadastro.html', context=context)
