from django import forms as django_forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from datetime import datetime
from .models import Fornecedor


class PasswordResetForm(auth_forms.PasswordResetForm):
    email = django_forms.EmailField(
        label="Email",
        max_length=254,
        widget=django_forms.EmailInput(attrs={"autocomplete": "email", 'placeholder': 'email@email.com'}),
    )


# Formulário utilizado no template de cadastro: /templates/cadastro.html
# Este formulário é utilizado para criação de novo usuário para realizar login
class UserCreationForm(auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Modificando os rótulos dos campos
        self.fields["username"].label = "Usuário"
        self.fields["email"].label = "Email"
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirme a Senha"
        self.fields["first_name"].label = "Nome"
        self.fields["last_name"].label = "Sobrenome"

        # Adicionando classes CSS aos widgets dos campos
        self.fields["username"].widget.attrs.update(
            {'class': 'border-dark text-muted', 'placeholder': 'Informe nome de usuário para realizar login'})
        self.fields["email"].widget.attrs.update(
            {'class': 'border-dark text-muted', 'placeholder': 'email@email.com'})
        self.fields["password1"].widget.attrs.update(
            {'class': 'border-dark', 'placeholder': 'Digite a senha'})
        self.fields["password2"].widget.attrs.update(
            {'class': 'border-dark', 'placeholder': 'Confirme a senha'})
        self.fields["first_name"].widget.attrs.update(
            {'class': 'border-dark text-muted', 'placeholder': 'Informe seu nome'})
        self.fields["last_name"].widget.attrs.update(
            {'class': 'border-dark text-muted', 'placeholder': 'Informe seu sobrenome'})


# Formulário utilizado no template de cadastro /templates/cadastro.html
class FornecedorForm(django_forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = "__all__"
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Modificando os rótulos dos campos
        self.fields["cpf_cnpj"].label = "CPF ou CNPJ"
        self.fields["nascimento"].label = "Data de nascimento"
        self.fields["dap"].label = "Número DAP"
        self.fields["prioritario"].label = "Você participa de algum grupo prioritário?"

        # Adicionando classes CSS aos widgets dos campos
        self.fields["cpf_cnpj"].widget.attrs.update(
            {'class': 'mask-cpf border-dark', 'placeholder': 'Somente números'})
        self.fields["telefone"].widget.attrs.update(
            {'class': 'mask-telefone border-dark', 'placeholder': 'Ex: (31) 91633-5643'})
        self.fields["cidade"].widget.attrs.update(
            {'class': 'border-dark', 'placeholder': 'Digite a cidade'})
        self.fields["estado"].widget.attrs.update(
            {'class': 'border-dark', 'placeholder': 'MG'})
        self.fields["endereco"].widget.attrs.update(
            {'class': 'border-dark', 'placeholder': 'Digite o endereço'})
        self.fields["bairro"].widget.attrs.update(
            {'class': 'border-dark', 'placeholder': 'Digite o bairro'})
        self.fields["dap"].widget.attrs.update(
            {'class': 'border-dark', 'placeholder': 'Digite o número da DAP (Declaração de Aptidão ao Pronaf)'})
        self.fields["associacao"].widget.attrs.update(
            {'class': 'border-dark', 'placeholder': 'PROV - PRODUTORES VIZINHOS'})
        self.fields["prioritario"].widget.attrs.update(
            {'class': 'border-dark'})

        # Modificando widget
        self.fields["nascimento"].widget = django_forms.DateInput(
            attrs={'type': 'date', 'max': datetime.now().date(), 'class': 'border-dark'}, format='%Y-%m-%d')
