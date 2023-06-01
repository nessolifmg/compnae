from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, FornecedorForm 



#----------------------- Usuários----------------------------#
def redirecionar(usuario,request): #Função para redirecionamento através dos grupos
    if usuario.groups.filter(name="fornecedor"):
        login(request, usuario)
        return redirect('/fornecedor')
    elif usuario.groups.filter(name="servidor"):
        login(request, usuario)
        return redirect('/servidor')   
    else:
        login(request, usuario)
        return redirect('/admin')

def logar_usuario(request): #Função de login de usuários
    if request.method == "GET":
        if request.user.is_authenticated:
           #Se o usuário for autenticado redireciona através da função para  a página correta
           return redirecionar(request.user, request)
        form_login = AuthenticationForm() 
    else:
        #Realiza a captura do login e senha através do post
        username = request.POST["username"]
        password = request.POST["password"]
        #Autentica o usuário
        usuario = authenticate(request, username=username, password=password)
        #Caso exista o usuário redirecioana através da função
        if usuario is not None :
            return redirecionar(usuario, request)
        else:
            form_login = AuthenticationForm()
            messages.error(request, "Usuário ou senha inválidos!")
    context = {
        'form_login': form_login
    }
    return render(request, 'login.html', context=context)

@login_required(login_url='/login/')
def logout_user(request): #Função de logout do sistema
    logout(request)
    return redirect('/')

def cadastrar_fornecedor(request): #Função para realizar o cadastro de fornecedores
    if request.method == "POST":
        #Faz uso dos formulários para facilitar a validação das informações
        form_usuario = UserCreationForm(request.POST)
        form_fornecedor = FornecedorForm(request.POST)
        if form_usuario.is_valid() and form_fornecedor.is_valid():
            usuario = form_usuario.save()
            #Adiciona o fornecedor cadastrado ao grupo fornecedor
            usuario.groups.add(Group.objects.get(name='fornecedor'))
            fornecedor = form_fornecedor.save(commit=False)
            fornecedor.user = usuario
            fornecedor.save()
            return redirect('/')
        else:
            context = {
                'form_usuario': form_usuario,
                'form_fornecedor': FornecedorForm
            }
    else:
        form_usuario = UserCreationForm()
        form_fornecedor = FornecedorForm()
        context = {
            'form_usuario': form_usuario,
            'form_fornecedor': FornecedorForm,
        }
    return render(request, 'cadastro.html', context=context)


