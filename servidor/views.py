from django.shortcuts import render, redirect
from django.db.models import Avg
from rolepermissions.decorators import has_role_decorator

from .forms import AlimentoForm, EditalForm, AlimentoNecessariosForm, AvisosForm
import fornecedor.models
from .models import Alimento, Edital, AlimentoNecessario

# Função para criar lista paginada de itens
from django.core.paginator import Paginator


def get_paginated_data(request, data_list):
    """
    Retorna uma página de dados paginados com base na solicitação HTTP e na lista de dados fornecida.
    """
    paginator = Paginator(data_list, 10)
    requested_page = request.GET.get('page')
    return paginator.get_page(requested_page)


@has_role_decorator('servidor')
def home_servidor(request):
    """
    View da página inicial para o grupo 'servidor'.
    Carrega e exibe alimentos necessários com edital ativo paginados.
    """
    alimentos_necessarios_list = (
        AlimentoNecessario.objects
        .order_by('alimento')
        .filter(edital__status=True)
        .select_related('alimento', 'edital')
    )
    context = {'alimentos': get_paginated_data(request, alimentos_necessarios_list)}
    return render(request, 'servidor.html', context=context)


@has_role_decorator('servidor')
def cadastrar_alimento(request):
    """
    View para cadastrar novos alimentos.
    """
    context = {}
    if request.method == "GET":
        alimentos_list = Alimento.objects.order_by('nome').all()
        form_alimento = AlimentoForm()
        context = {
            'form_alimento': form_alimento,
            'alimentos': get_paginated_data(request, alimentos_list)
        }
    elif request.method == "POST":
        form_alimento = AlimentoForm(request.POST)
        alimentos_list = Alimento.objects.order_by('nome').all()
        if form_alimento.is_valid():
            form_alimento.save()
            form_alimento = AlimentoForm()
        context = {
            'form_alimento': form_alimento,
            'alimentos': get_paginated_data(request, alimentos_list)
        }
    return render(request, 'cadastro_alimentos.html', context=context)


@has_role_decorator('servidor')
def atualizar_alimento(request, alimento_id):
    """
        View para atualizar dados de um alimento existente.
    """
    context = {}
    if request.method == "GET":
        alimento = Alimento.objects.filter(id=alimento_id).first()
        form_alimento = AlimentoForm(instance=alimento)
        alimentos_list = Alimento.objects.order_by('nome').all()
        context = {
            'form_alimento': form_alimento,
            'alimentos': get_paginated_data(request, alimentos_list)
        }
    elif request.method == "POST":
        alimento = Alimento.objects.filter(id=alimento_id).first()
        form_alimento = AlimentoForm(request.POST, instance=alimento)
        if form_alimento.is_valid():
            form_alimento.save()
            # /servidor/cadastro/alimentos/
            return redirect('cadastro_alimentos')
        else:
            alimentos_list = Alimento.objects.order_by('nome').all()
            context = {
                'form_alimento': form_alimento,
                'alimentos': get_paginated_data(request, alimentos_list)
            }
    return render(request, 'cadastro_alimentos.html', context=context)


@has_role_decorator('servidor')
def cadastrar_edital(request):
    """
        View para cadastrar editais.
    """
    context = {}
    if request.method == "GET":
        # Busca todos os editais e ordena em ordem decrescente pela data de início
        editais_list = Edital.objects.order_by('-data_inicio').all()
        form_edital = EditalForm()
        context = {
            'form_edital': form_edital,
            'editais': get_paginated_data(request, editais_list)
        }
    elif request.method == "POST":
        # Cria um formulário com os dados do edital retornados pelo POST do template
        form_edital = EditalForm(request.POST)
        editais_list = Edital.objects.order_by('-data_inicio').all()

        if form_edital.is_valid():
            form_edital.save()
            form_edital = EditalForm()

        context = {
            'form_edital': form_edital,
            'editais': get_paginated_data(request, editais_list)
        }
    return render(request, 'cadastro_editais.html', context=context)


@has_role_decorator('servidor')
def atualizar_edital(request, edital_id):
    """
        View para atualizar editais.
    """
    context = {}
    if request.method == "GET":
        # Busca todos os editais e ordena em ordem decrescente pela data de início
        editais_list = Edital.objects.order_by('-data_inicio').all()
        # Filtra o edital pelo edital_id passado por argumento na URL
        edital = editais_list.filter(id=edital_id).first()
        # Cria um formulário com a instância do edital retornado
        form_edital = EditalForm(instance=edital)
        context = {
            'form_edital': form_edital,
            'editais': get_paginated_data(request, editais_list)
        }
    elif request.method == "POST":
        # Busca o edital pelo edital_id passado na URL
        edital = Edital.objects.filter(id=edital_id).first()
        # Cria uma instância de edital com os novos dados passados pelo POST
        form_edital = EditalForm(request.POST, instance=edital)
        if form_edital.is_valid():
            form_edital.save()
            return redirect('cadastro_editais')  # Redireciona após sucesso
        else:
            editais_list = Edital.objects.order_by('-data_inicio').all()
            context = {
                'form_edital': form_edital,
                'editais': get_paginated_data(request, editais_list)
            }
    return render(request, 'cadastro_editais.html', context=context)


@has_role_decorator('servidor')
def cadastrar_alimento_necessario(request):
    """
    View para cadastrar novos alimentos necessários.
    """
    context = {}  # Inicializa o contexto vazio
    if request.method == "GET":
        # Busca todos os alimentos necessários ordenados pelo nome e filtra os que possuem edital ativo
        alimentos_necessarios_list = AlimentoNecessario.objects.order_by('alimento').filter(
            edital__status=True).select_related('alimento', 'edital')
        form_alimento_necessario = AlimentoNecessariosForm()
        # Preenche o contexto com o formulário vazio e os dados paginados
        context = {
            'form_alimento_necessario': form_alimento_necessario,
            'alimentos_necessarios_pag': get_paginated_data(request, alimentos_necessarios_list)
        }
    elif request.method == "POST":
        # Cria formulário com os dados do alimento necessário retornado pelo POST do template
        alimentos_necessarios_list = AlimentoNecessario.objects.order_by('alimento').filter(
            edital__status=True).select_related('alimento', 'edital')
        form_alimento_necessario = AlimentoNecessariosForm(request.POST)
        if form_alimento_necessario.is_valid():
            form_alimento_necessario.save()
            form_alimento_necessario = AlimentoNecessariosForm()
        context = {
            'form_alimento_necessario': form_alimento_necessario,
            'alimentos_necessarios_pag': get_paginated_data(request, alimentos_necessarios_list)
        }
    return render(request, 'cadastro_alimentos_necessarios.html', context=context)


@has_role_decorator('servidor')
def deletar_alimento_necessario(request, alimento_necessario_id):
    try:
        # Tenta encontrar e excluir o AlimentoNecessario com o ID fornecido
        alimento_necessario = AlimentoNecessario.objects.get(pk=alimento_necessario_id)
        alimento_necessario.delete()
    except AlimentoNecessario.DoesNotExist:
        # Se não encontrar o objeto, redireciona para a página de cadastro de alimentos necessários
        return redirect('cadastrar_alimento_necessario')

    # Redireciona de volta para a página de cadastro de alimentos necessários após a exclusão bem-sucedida
    return redirect('cadastrar_alimento_necessario')


@has_role_decorator('servidor')
def media_alimentos(request):
    """
    View para calcular a média de preço dos alimentos fornecidos.
    """
    context = {}  # Inicializa o contexto vazio

    if request.method == "GET" or request.method == "POST":
        # Dicionario para calculo da media do preço dos alimentos fornecidos
        media_alimento = {}
        alimentos_fornecidos_edital = None
        alimentos_necessarios = None
        if request.method == "GET":
            # Busca os alimentos_fornecidos pelo edital ativo
            alimentos_fornecidos_edital = fornecedor.models.AlimentoFornecido.objects.filter(
                fornecedor_edital__edital__status=True).select_related('fornecedor_edital', 'alimento')
            # Busca os alimentos necessarios do edital ativo
            alimentos_necessarios = AlimentoNecessario.objects.order_by('id').filter(edital__status=True)
        elif request.method == "POST":
            # seleciona o id do edital selecionado no select para filtro
            edital_id = request.POST.get('select_editais')
            # busca o edital selecionado
            edital = Edital.objects.filter(id=int(edital_id)).first()
            # busca os alimentos fornecidos no edital selecionado
            alimentos_fornecidos_edital = fornecedor.models.AlimentoFornecido.objects.filter(
                fornecedor_edital__edital=edital).select_related('fornecedor_edital', 'alimento')
            # Busca os alimentos necessarios do edital
            alimentos_necessarios = AlimentoNecessario.objects.order_by('alimento').filter(edital=edital)

        # Loop para alimentar o dicionario da media de alimentos
        for alimento_fornecido in alimentos_fornecidos_edital:
            # Pega a quantidade requerida de alimentos necessarios
            try:
                qtd = alimentos_necessarios.get(alimento=alimento_fornecido.alimento).quantidade
            except AlimentoNecessario.DoesNotExist:
                qtd = 0
            # Coloca no dicionário com chave com nome do alimento, valor array [media, quantidade]
            media_alimento[str(alimento_fornecido.alimento)] = [
                alimentos_fornecidos_edital.filter(alimento=alimento_fornecido.alimento).aggregate(
                    Avg('preco'))['preco__avg'], qtd
            ]

        # Busca todos editais para serem mostrados no filtro select
        editais = Edital.objects.all()

        # Preenche o contexto com as informações necessárias
        context = {
            'editais': editais,
            'alimentos': get_paginated_data(request, list(media_alimento.items())),
        }
    return render(request, 'media_alimentos.html', context=context)


@has_role_decorator('servidor')
def lista_fornecedores(request):
    alimentos_list = None
    if request.method == "GET":
        alimentos_list = fornecedor.models.FornecedorEdital.objects.order_by('id').all()
    elif request.method == "POST":
        forn = request.POST.get('input-fornecedores')
        alimentos_list = fornecedor.models.FornecedorEdital.objects.filter(user__user__first_name=forn)

    context = {
        'alimentos': get_paginated_data(request, alimentos_list)
    }
    return render(request, 'lista_fornecedores.html', context=context)


@has_role_decorator('servidor')
def gerenciar_avisos(request):
    form_avisos = AvisosForm()
    if request.method == "POST":
        form_avisos = AvisosForm(request.POST)
        if form_avisos.is_valid():
            form_avisos.save()
            form_avisos = AvisosForm()
    context = {
        'form_avisos': form_avisos,
    }
    return render(request, 'gerenciar_avisos.html', context=context)
