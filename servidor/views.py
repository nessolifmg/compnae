from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg

from .forms import AlimentoForm, EditalForm, AlimentoNecessariosForm, AvisosForm
from fornecedor.models import AlimentoFornecido, FornecedorEdital
from .models import Alimento, Edital, AlimentoNecessario

#Função para criar lista paginada de itens
def paginator(request, list):
    paginator = Paginator(list, 10)
    page = request.GET.get('page')
    return paginator.get_page(page)

@login_required(login_url='/login/')
def home_servidor(request):
    #verifica se usuario faz parte do grupo servidor
    if request.user.groups.filter(name='servidor'):
        #Busca os alimentos necessarios
        #Busca todos alimentos necessarios ordenados pelo nome e filtra os que possuem edital ativo
        alimentos_necessarios_list = AlimentoNecessario.objects.order_by(
                'alimento').filter(
                edital__status=True,
                ).select_related('alimento', 'edital')
        #Dicionario com os dados paginados para ser mostrado no template 
        context = {
            'alimentos': paginator(request, alimentos_necessarios_list) 
        }
        return render(request, 'servidor.html', context=context) 
    else: 
        #Redireciona para pagina inicial ao usuario pertence de acordo com grupo
        return redirect('/')
#----------------------- Alimentos----------------------------#

@login_required(login_url='/login/')
def cadastrar_alimento(request):
    #verifica se usuario faz parte do grupo servidor
    if request.user.groups.filter(name='servidor'):
        if request.method == "GET":
            #Busca todos alimentos ordenados pelo id
            #Cria formulario vazio para cadastro de alimentos
            alimentos_list = Alimento.objects.order_by('nome').all()
            form_alimento = AlimentoForm()
            
            #Dicionario com formulario vazio
            #Dados paginados para ser mostrado no template
            context = {
                'form_alimento': form_alimento,
                'alimentos': paginator(request, alimentos_list) 
            }

        elif request.method == "POST":
            #Cria formulario com os dados do alimento retornado pelo POST do template
            form_alimento = AlimentoForm(request.POST)
            if form_alimento.is_valid(): #Verifica se é valido, validação ocorre em forms.py
                form_alimento.save() 
                #Após alimento salvo cria um form vazio para ser passado novamente para o template
                form_alimento = AlimentoForm()
                #Busca os alimentos inclusive o salvo anteriomente para ser mostrado no template
                alimentos_list = Alimento.objects.order_by('nome').all()
                #Dicionario com formulario vazio
                #Dados paginados para ser mostrado no template
                context = {
                    'form_alimento': form_alimento,
                    'alimentos': paginator(request, alimentos_list)
                }
            #Se formulario não foi valido
            else:
                alimentos_list = Alimento.objects.order_by('nome').all()
                #Dicionario com formulario com erros ocasionados pela validação
                #Dados paginados para ser mostrado no template
                context = {
                    'form_alimento': form_alimento,
                    'alimentos': paginator(request, alimentos_list)
                }
        
        return render(request, 'cadastro_alimentos.html', context=context)
    else:
        return redirect('/')

@login_required(login_url='/login/')
def atualizar_alimento(request, alimento_id):
    #Verifica se usuario faz parte do grupo servidor
    if request.user.groups.filter(name='servidor'):
        if request.method == "GET":
            #Busca todos alimentos
            alimentos_list = Alimento.objects.order_by('nome').all()
            #Filtra alimento pelo alimento_id passado por argumento na url
            #Busca na consulta realizada anteriormente
            alimento = alimentos_list.filter(id=alimento_id).first()
            #Cria formulario com instancia do alimento retornado
            form_alimento = AlimentoForm(instance=alimento)
            #Dicionario com formulario preenchido com instancia do alimento
            #Dados paginados para ser mostrado no template
            context = {
                'form_alimento': form_alimento,
                'alimentos': paginator(request, alimentos_list)
            }

        elif request.method == "POST":
            #Busca o alimento pelo alimento_id passado pela url
            alimento = Alimento.objects.filter(id=alimento_id).first()
            #Cria um instancia de alimento pelo novos dados passado pelo POST
            #E atualiza a instancia buscada no banco pela pk
            form_alimento = AlimentoForm(request.POST, instance=alimento)
            if form_alimento.is_valid():
                form_alimento.save()
                 #Após alimento salvo cria um form vazio para ser passado novamente para o template
                form_alimento = AlimentoForm()
                #Busca os alimentos inclusive o atualizado anteriomente para ser mostrado no template
                alimentos_list = Alimento.objects.order_by('nome').all()
                #Dicionario com formulario vazio
                #Dados paginados para ser mostrado no template
                context = {
                    'form_alimento': form_alimento,
                    'alimentos': paginator(request, alimentos_list)
                }
                #Se alimento atualizado redireciona para url padrão
                #/servidor/cadastro/alimentos/
                return redirect('cadastro_alimentos')
            #Se formulario não foi valido
            else:
                alimentos_list = Alimento.objects.order_by('nome').all()
                #Dicionario com formulario com erros ocasionados pela validação
                #Dados paginados para ser mostrado no template
                context = {
                    'form_alimento': form_alimento,
                    'alimentos': paginator(request, alimentos_list)
                }

        return render(request, 'cadastro_alimentos.html', context=context)
    else:
        return redirect('/')
#----------------------- Editais ----------------------------#

@login_required(login_url='/login/')
def cadastrar_edital(request):
    #Verifica se usuario faz parte do grupo servidor
    if request.user.groups.filter(name='servidor'):
        if request.method == "GET":
            #Busca todos editais ordenados descedente pela data
            editais_list = Edital.objects.order_by('-data_inicio').all()
            form_edital = EditalForm()
            #Dicionario com formulario vazio
            #Dados paginados para ser mostrado no template
            context = {
                'form_edital' : form_edital,
                'editais': paginator(request, editais_list)
            }
           
        elif request.method == "POST": 
             #Cria formulario com os dados do edital retornado pelo POST do template 
            form_edital = EditalForm(request.POST)
            if form_edital.is_valid():
                form_edital.save()
                #Após edital salvo cria um form vazio para ser passado novamente para o template
                form_edital = EditalForm()
                #Busca os editais inclusive o salvo anteriomente para ser mostrado no template
                editais_list = Edital.objects.order_by('-data_inicio').all()
                #Dicionario com formulario vazio
                #Dados paginados para ser mostrado no template
                context = {
                    'form_edital': form_edital,
                    'editais': paginator(request, editais_list)
                }
            #Se formulario não foi valido
            else:
                editais_list = Edital.objects.order_by('-data_inicio').all()
                #Dicionario com formulario com erros ocasionados pela validação
                #Dados paginados para ser mostrado no template
                context = {
                    'form_edital' : form_edital,
                    'editais': paginator(request, editais_list)
                }
        return render(request , 'cadastro_editais.html', context=context)
    else: 
        return redirect('/')


@login_required(login_url='/login/')
def atualizar_edital(request, edital_id):
     #Verifica se usuario faz parte do grupo servidor
    if request.user.groups.filter(name='servidor'):
        if request.method == "GET":
            #Busca todos editais ordenados descedente pela data
            editais_list = Edital.objects.order_by('-data_inicio').all()
            #Filtra alimento pelo alimento_id passado por argumento na url
            #Busca na consulta realizada anteriormente
            edital = editais_list.filter(id=edital_id).first()
            #Cria formulario com instancia do edital retornado
            form_edital = EditalForm(instance=edital)
            #Dicionario com formulario preenchido com instancia do edital
            #Dados paginados para ser mostrado no template
            context = {
                'form_edital' : form_edital,
                'editais' : paginator(request, editais_list)
            }
           
        elif request.method == "POST":
            #Busca o edital pelo alimento_id passado pela url
            edital = Edital.objects.filter(id=edital_id).first()
            #Cria um instancia de edital pelos novos dados passado pelo POST
            #E atualiza a instancia buscada no banco pela pk
            form_edital = EditalForm(request.POST, instance=edital)
            if form_edital.is_valid():
                form_edital.save()
                 #Após edital salvo cria um form vazio para ser passado novamente para o template
                form_edital = EditalForm()
                #Busca os editais inclusive o atualizado anteriomente para ser mostrado no template
                editais_list = Edital.objects.order_by('-data_inicio').all()
                #Dicionario com formulario vazio
                #Dados paginados para ser mostrado no template
                context = {
                    'form_edital': form_edital,
                    'editais': paginator(request, editais_list)
                }
                #Se edital atualizado redireciona para url padrão
                #/servidor/cadastro/editais/
                return redirect('cadastro_editais')
            #Se formulario não foi valido
            else:
                editais_list = Edital.objects.order_by('-data_inicio').all()
                #Dicionario com formulario com erros ocasionados pela validação
                #Dados paginados para ser mostrado no template
                context = {
                    'form_edital': form_edital,
                    'editais': paginator(request, editais_list)
                }

        return render(request, 'cadastro_editais.html', context=context)
    else:
        return redirect('/')

#----------------------- Alimentos por edital ----------------------------#
@login_required(login_url='/login/')
def cadastrar_alimento_necessario(request):
    #Verifica se usuario faz parte do grupo servidor
    if request.user.groups.filter(name='servidor'):
        if request.method == "GET":
            #Busca todos alimentos necessarios ordenados pelo nome e filtra os que possuem edital ativo
            alimentos_necessarios_list = AlimentoNecessario.objects.order_by(
                'alimento').filter(
                edital__status=True,
                ).select_related('alimento', 'edital')
            form_alimento_necessario = AlimentoNecessariosForm()
            #Dicionario com alimentos para serem selecionado
            # com formulario vazio
            #Dados paginados para ser mostrado no template
            context = {
                'form_alimento_necessario': form_alimento_necessario,
                'alimentos_necessarios_pag': paginator(request, alimentos_necessarios_list)
            }
            
        elif request.method == "POST": 
            #Cria formulario com os dados do alimento necessario 
            # retornado pelo POST do template 
            form_alimento_necessario = AlimentoNecessariosForm(request.POST)
            if form_alimento_necessario.is_valid():
                form_alimento_necessario.save()
                #Após alimento necessario salvo cria um form vazio para ser passado novamente para o template
                form_alimento_necessario = AlimentoNecessariosForm()
                #Busca os alimentos necessarios inclusive o salvo anteriomente para ser mostrado no template
                alimentos_necessarios_list = AlimentoNecessario.objects.order_by(
                'alimento').filter(
                edital__status=True
                ).select_related('alimento', 'edital')
                #Dicionario com alimentos para serem selecionado
                #com formulario vazio
                #Dados paginados para ser mostrado no template
                context = {
                    'form_alimento_necessario': form_alimento_necessario,
                    'alimentos_necessarios_pag': paginator(request, alimentos_necessarios_list)
                }
            #Se formulario não foi valido 
            else:
                alimentos_necessarios_list = AlimentoNecessario.objects.order_by(
                'alimento').filter(
                edital__status=True
                ).select_related('alimento', 'edital')
                context = {
                    'form_alimento_necessario': form_alimento_necessario,
                    'alimentos_necessarios_pag': paginator(request, alimentos_necessarios_list)
                }
        return render(request, 'cadastro_alimentos_necessarios.html', context= context)
    else: 
        return redirect('/')

@login_required(login_url='/login/')
def deletar_alimento_necessario(request, alimento_necessario_id):
    if request.user.groups.filter(name='servidor'):
        try:
            AlimentoNecessario.objects.filter(id=alimento_necessario_id).first().delete()  
        except Exception:
            return redirect('cadastrar_alimento_necessario') 
              
        return redirect('cadastrar_alimento_necessario') 
    else: 
        return redirect('/')

@login_required(login_url='/login/')
def media_alimentos(request):
    #Verifica se usuario faz parte do grupo servidor
    if request.user.groups.filter(name='servidor'): 
        if request.method == "GET":
            #Dicionario para calculo da media do preço dos alimentos fornecidos
            media_alimento = {}
            #Busca os alimentos_fornecidos pelo edital ativo
            alimentos_fornecidos_edital = AlimentoFornecido.objects.filter(
                fornecedor_edital__edital__status=True).select_related('fornecedor_edital', 'alimento')
            #Busca os alimentos necessarios do edital ativo
            alimentos_necessarios = AlimentoNecessario.objects.order_by('id').filter(edital__status=True)
            #Loop para alimentar o dicionario da media de alimentos
            for alimento_fornececido in alimentos_fornecidos_edital: 
                #Pega a quantidade requerida de alimentos necessarios
                qtd = alimentos_necessarios.get(alimento=alimento_fornececido.alimento).quantidade
                #Coloca no dicionario com chave com nome do alimento, valor array [media, quantidade] 
                media_alimento[str(alimento_fornececido.alimento)] = [alimentos_fornecidos_edital.filter(
                    alimento=alimento_fornececido.alimento).aggregate(Avg('preco'))['preco__avg'], qtd]
            #Busca todos editais para ser mostrado no filtro select
            editais = Edital.objects.all()
             #Dicionario com editais para serem selecionados
            #Dados paginados para ser mostrado no template
            context = {
                'editais': editais,
                #É precido converter o dicionario em uma lista para ser paginado
                'alimentos': paginator(request, list(media_alimento.items())),
            }
           
        elif request.method == "POST":
            #Dicionario para calculo da media do preço dos alimentos fornecidos
            media_alimento = {}
            #seleciona o id do edital selecionado no select para filtro
            edital_id = request.POST.get('select_editais')
            #busca o edital selecionado 
            edital = Edital.objects.filter(id=int(edital_id)).first()
            #busca os alimentos fornecidos no edital selecionado
            alimentos_fornecidos_edital = AlimentoFornecido.objects.filter(
                fornecedor_edital__edital=edital).select_related('fornecedor_edital', 'alimento')
            #Busca os alimentos necessarios do edital
            alimentos_necessarios = AlimentoNecessario.objects.order_by('alimento').filter(edital=edital)
            #Loop para alimentar o dicionario da media de alimentos
            for alimento_fornececido in alimentos_fornecidos_edital: 
                #Pega a quantidade requerida de alimentos necessarios
                qtd = alimentos_necessarios.get(alimento=alimento_fornececido.alimento).quantidade
                #Coloca no dicionario com chave com nome do alimento, valor array [media, quantidade] 
                media_alimento[str(alimento_fornececido.alimento)] = [alimentos_fornecidos_edital.filter(
                    alimento=alimento_fornececido.alimento).aggregate(Avg('preco'))['preco__avg'], qtd]
            #Busca todos editais para ser mostrado no filtro select
            editais = Edital.objects.all()
             #Dicionario com editais para serem selecionados
            #Dados paginados para ser mostrado no template
            context = {
                'editais': editais,
                #É precido converter o dicionario em uma lista para ser paginado
                'alimentos': paginator(request, list(media_alimento.items())),
            }
        return render(request, 'media_alimentos.html', context=context)
    else: 
        return redirect('/')

def lista_fornecedores(request):
    if request.user.groups.filter(name='servidor'):
        if request.method == "GET":
            
            alimentos_list = FornecedorEdital.objects.order_by('id').all()   
            #Dicionario com formulario vazio
            #Dados paginados para ser mostrado no template
            context = {
                'alimentos': paginator(request, alimentos_list) 
            }
        elif request.method == "POST":

            fornecedor = request.POST.get('input-fornecedores')
            alimentos_list = FornecedorEdital.objects.filter(user__user__first_name=fornecedor)
            
            #Dicionario com formulario vazio
            #Dados paginados para ser mostrado no template
            context = {
                'alimentos': paginator(request, alimentos_list) 
            }
    return render(request, 'lista_fornecedores.html', context=context)

def gerenciar_avisos(request):
    if request.user.groups.filter(name='servidor'):
        if request.method == "GET":
            form_avisos = AvisosForm()
            context = {
                'form_avisos': form_avisos,
            }
        elif request.method == "POST": 
            form_avisos = AvisosForm(request.POST)
            if form_avisos.is_valid():
                form_avisos.save()
                form_avisos = AvisosForm()
            context = {
                'form_avisos': form_avisos,
            }
    return render(request, 'gerenciar_avisos.html', context=context)