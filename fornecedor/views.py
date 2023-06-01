from multiprocessing import context
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from core.forms import UserCreationForm, FornecedorForm 

from servidor.models import Edital
from .models import *


@login_required(login_url='/login/')
def home_fornecedor(request):
    #verifica se usuario faz parte do grupo servidor
    if request.user.groups.filter(name='fornecedor'):
        alimentos_necessarios_list = AlimentoNecessario.objects.filter(edital__status = True).order_by('id')

        paginator = Paginator(alimentos_necessarios_list, 10)
        page = request.GET.get('page')
        alimentos_necessarios = paginator.get_page(page)

        #Dicionario com os dados paginados para ser mostrado no template
        context = {
            'alimentos': alimentos_necessarios
        }
        #Redireciona para pagina inicial do fornecedor 
        return render(request, 'fornecedor.html', context=context) 
    else: 
        #Redireciona para pagina inicial ao usuario pertence de acordo com grupo
        return redirect('/')

def fornecer_alimentos(request):  #Utilizada para carregar a página de fornecimento de alimentos
    if request.user.groups.filter(name='fornecedor'):
        user = Fornecedor.objects.get(user = request.user) 
        #Evita o fornecimento repetido de um fornecedor
        if(not FornecedorEdital.objects.filter(user = user)):
            #Cria uma lista dos alimentos necessários
            alimentos_necessarios = AlimentoNecessario.objects.all()
            #Cria um dicionário
            dados = {'alimentos': alimentos_necessarios}
            return render(request, 'fornecer_alimentos.html', dados) 
        else:
            return redirect('/')
    else: 
        return redirect('/')

@require_POST
def submit_fornecer_alimentos(request): #Utilizada para cadastrar os alimentos fornecidos
    if request.user.groups.filter(name='fornecedor'):
        if request.POST:
            #Cria um objeto usuário a partir da requisição
            user = Fornecedor.objects.get(user=request.user)
            #Cria um objeto edital a partir da requisição 
            edital = Edital.objects.get(numero=request.POST.get("edital"))
            #cria um fornecedor por Edital a partir dos objetos anteriores
            fornecedor = FornecedorEdital.objects.create(user=user, edital=edital)
            fornecedor.save()
            
            nf = AlimentoNecessario.objects.filter()
            for a in nf:
                if a.edital.status:
                    #Realiciona o alimento fornecido ao fornecedor por edital 
                    if request.POST.get(str(a.id))!='':
                        AlimentoFornecido.objects.create(fornecedor_edital=fornecedor, alimento=a.alimento, 
                        preco=request.POST.get(str(a.id))).save()

            return redirect("/fornecedor")
    else: 
        return redirect('/')

def perfil (request): #Carrega as informações do usuário cadastrado
    if request.user.groups.filter(name='fornecedor'):
        #Faz uso dos forms do cadastro
        if request.method == 'GET':
            print('get')
            usuario = request.user 
            fornecedor = Fornecedor.objects.get(user_id = request.user)
            form_usuario = UserCreationForm(instance = usuario)
            form_fornecedor = FornecedorForm(instance = fornecedor)
            context = {
                'form_usuario': form_usuario,
                'form_fornecedor': form_fornecedor,
            }
        elif request.method == "POST":
            print('post')
            usuario = request.user 
            fornecedor = Fornecedor.objects.get(user_id = request.user)
            form_usuario = UserCreationForm(request.POST, instance = usuario)
            form_fornecedor = FornecedorForm(request.POST, instance = fornecedor)
            if form_usuario.is_valid() and form_fornecedor.is_valid():
                form_usuario.save()
                form_fornecedor.save()
            context = {
                'form_usuario': form_usuario,
                'form_fornecedor': form_fornecedor,
            }
        return render(request, 'perfil.html', context=context) 
    else: 
        return redirect('/')
