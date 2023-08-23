from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.http import HttpResponse
from rolepermissions.decorators import has_role_decorator
from .models import FornecedorEdital, AlimentoFornecido
import core.forms
import servidor.models


# Decorator para verificar se o usuário faz parte das permissões de 'fornecedor'
@has_role_decorator('fornecedor')
def home_fornecedor(request):
    # Obter uma lista dos alimentos necessários onde edital__status é True e ordená-los pelo ID
    food_necessary_list = servidor.models.AlimentoNecessario.objects.filter(edital__status=True).order_by('id')
    # Criar um objeto Paginator para paginar a lista de alimentos necessários com 10 itens por página
    paginator = Paginator(food_necessary_list, 10)
    # Obtendo o número da página atual a partir dos parâmetros da requisição (GET)
    page = request.GET.get('page')
    # Obtendo os alimentos necessários para a página atual usando o objeto Paginator
    food_necessary = paginator.get_page(page)

    # Criando um dicionário com os dados paginados para serem passados ao template para renderização
    context = {
        'alimentos': food_necessary
    }
    # Renderizando o template 'fornecedor.html' com os dados paginados
    return render(request, 'fornecedor.html', context=context)


# Decorator para verificar se o usuário faz parte das permissões de 'fornecedor'
@has_role_decorator(role='fornecedor')
def fornecer_alimentos(request):
    # Obtendo o objeto do fornecedor associado ao usuário logado
    user = core.models.Fornecedor.objects.get(user=request.user)
    # Verifica se o fornecedor já realizou o fornecimento anteriormente
    if not FornecedorEdital.objects.filter(user=user, edital__status=True):
        # Criando uma lista com todos os alimentos necessários cadastrados
        food_necessary = servidor.models.AlimentoNecessario.objects.all()
        # Criando um dicionário para enviar os dados dos alimentos necessários ao template
        context = {
            'alimentos': food_necessary
        }
        # Renderizando a página 'fornecer_alimentos.html' com os dados dos alimentos necessários
        return render(request, 'fornecer_alimentos.html', context=context)
    else:
        # Exibe uma mensagem caso o fornecedor já tenha fornecido anteriormente
        return HttpResponse('Alimentos já submetidos no edital')


# Decorator para verificar se o usuário faz parte das permissões de 'fornecedor'
@has_role_decorator('fornecedor')
def submit_fornecer_alimentos(request):
    """
        Esta visão lida com a submissão de alimentos pelo fornecedor.
    """
    if request.method == 'POST':
        # Obtendo o objeto fornecedor associado ao usuário logado
        user = core.models.Fornecedor.objects.get(user=request.user)
        # Obtendo o objeto edital com base no número fornecido no formulário
        edital_number = request.POST.get("edital")
        edital = servidor.models.Edital.objects.get(numero=edital_number)

        # Criando um novo fornecedor por edital usando os objetos obtidos acima
        fornecedor = FornecedorEdital.objects.create(user=user, edital=edital)

        # Percorrendo todos os alimentos necessários
        food_necessary_list = servidor.models.AlimentoNecessario.objects.all()
        for food_necessary in food_necessary_list:
            if food_necessary.edital.status:
                # Relaciona o alimento fornecido ao fornecedor por edital
                food_price = request.POST.get(str(food_necessary.id))
                if food_price != '':
                    AlimentoFornecido.objects.create(fornecedor_edital=fornecedor,
                                                     alimento=food_necessary.alimento,
                                                     preco=food_price)
        # Renderizando a página 'fornecer_alimentos.html' com os dados dos alimentos necessários
        return redirect("/fornecedor")


# Decorator para verificar se o usuário faz parte das permissões de 'fornecedor'
@has_role_decorator('fornecedor')
def perfil(request):
    """
        Esta visão lida com a página de perfil do usuário.
    """
    # Obtendo o usuário conectado.
    user = request.user

    # Tenta obter o objeto do fornecedor relacionado ao usuário.
    try:
        fornecedor = core.models.Fornecedor.objects.get(user_id=user)
    except core.models.Fornecedor.DoesNotExist:
        fornecedor = None

    if request.method == 'POST':
        # Obter os formulários de usuário e fornecedor dos dados da solicitação.
        form_user = core.forms.UserCreationForm(request.POST, instance=user)
        form_fornecedor = core.forms.FornecedorForm(request.POST, instance=fornecedor)

        # Se ambos os formulários forem válidos, salve-os.
        if form_user.is_valid() and form_fornecedor.is_valid():
            form_user.save()
            form_fornecedor.save()
    else:
        form_user = core.forms.UserCreationForm(instance=user)
        form_fornecedor = core.forms.FornecedorForm(instance=fornecedor)

    # Crie o dicionário de contexto para o modelo.
    context = {
        'form_usuario': form_user,
        'form_fornecedor': form_fornecedor,
    }
    # Renderizando a página 'fornecer_alimentos.html' com os dados dos alimentos necessários
    return render(request, 'perfil.html', context=context)
