from datetime import datetime
from django import forms as django_forms
from django.contrib.auth import forms
from django.contrib.auth.models import User

from datetime import datetime
from .models import Fornecedor

class PasswordResetForm(forms.PasswordResetForm):
    email = django_forms.EmailField(
        label=("Email"),
        max_length=254,
        widget=django_forms.EmailInput(attrs={"autocomplete": "email", 'placeholder': 'email@email.com'}),
    )


class FornecedorForm(django_forms.ModelForm):
   
    class Meta:
        model = Fornecedor
        fields = "__all__"
        exclude = ['user']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cpf_cnpj"].widget.attrs.update({'class': 'mask-cpf border-dark','placeholder': '999.999.999-99'})
        self.fields["telefone"].widget.attrs.update({'class': 'mask-telefone border-dark', 'placeholder': '(31) 91633-5643'})
        self.fields["cidade"].widget.attrs.update({'class':'border-dark', 'placeholder': 'Bambuí'})
        self.fields["estado"].widget.attrs.update({'class':'border-dark', 'placeholder': 'MG'})
        self.fields["endereco"].widget.attrs.update({'class':'border-dark', 'placeholder': 'Rua das laranjeiras, 77'})
        self.fields["bairro"].widget.attrs.update({'class':'border-dark', 'placeholder': 'Rola moça'})
        self.fields["nascimento"].widget = django_forms.DateInput(attrs={'type': 'date', 'max': datetime.now().date() , 'class':'border-dark'}, format='%Y-%m-%d')
        self.fields["dap"].widget.attrs.update({'class':'border-dark', 'placeholder': 'Número da DAP'})
        self.fields["associacao"].widget.attrs.update({'class':'border-dark', 'placeholder': 'PROV - PRODUTORES VIZINHOS'})
        self.fields["prioritario"].widget.attrs.update({'class':'border-dark'})
        self.fields["prioritario"].label = "Você participa de algum grupo prioritário?"

class UserCreationForm(forms.UserCreationForm):
    first_name = django_forms.CharField(widget=django_forms.TextInput(attrs= {'class':'border-dark', 'placeholder': 'José'}))
    last_name = django_forms.CharField(widget=django_forms.TextInput(attrs= {'class':'border-dark', 'placeholder': 'da Silva'}))
    email = django_forms.EmailField(widget=django_forms.TextInput(attrs={'class':'border-dark', 'placeholder':'email@email.com'}))
   
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email",  ) 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #label
        self.fields["username"].label = "Usuário"
        self.fields["first_name"].label = "Nome"
        self.fields["last_name"].label = "Sobrenome"
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirme a Senha"
        #widget
        self.fields["username"].widget.attrs.update({'class':'border-dark text-muted', 'placeholder':'josesilva12'}) 
        self.fields["password1"].widget.attrs.update({'class':'border-dark'}) 
        self.fields["password2"].widget.attrs.update({'class':'border-dark'})
        #help_text
        self.fields["username"].help_text = "Letras, números e @/./+/-/_ apenas, será usado para login."
        self.fields["password1"].help_text ="Sua senha deve ter de 8 a 20 caracteres."  

