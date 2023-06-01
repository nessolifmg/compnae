from django import forms 
from django.core.exceptions import ValidationError
from .models import Alimento, Edital, AlimentoNecessario, Avisos

from datetime import datetime

class AlimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(AlimentoForm, self).__init__(*args, **kwargs)
        self.fields["nome"].label = "Nome do Alimento"
        self.fields["nome"].widget =forms.TextInput(attrs= {'placeholder': 'BATATA', 'style' :'text-transform: uppercase' , 'class':'border-dark'})

    def clean_nome(self):
        nome = self.cleaned_data['nome']
        return nome.upper()

class EditalForm(forms.ModelForm):
    class Meta:
        model = Edital
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(EditalForm, self).__init__(*args, **kwargs)
        self.fields["status"].label = "Ativar Edital"
        self.fields["data_inicio"].label = "Data de Inicio"
        self.fields["data_final"].label = "Data de Término"
        self.fields["data_inicio"].widget = forms.DateInput(attrs={'type': 'date', 'class':'border-dark'}, format='%Y-%m-%d' )
        self.fields["data_final"].widget = forms.DateInput(attrs={'type': 'date', 'class':'border-dark'}, format='%Y-%m-%d' )
        self.fields["numero"].widget.attrs.update({'class': 'border-dark', 'placeholder':'2022/1'})
        self.fields["status"].widget = forms.CheckboxInput(attrs={'class': 'form-check-input border-dark', 'type': 'checkbox'})
    
    def clean_status(self):
        status = self.cleaned_data['status']
        if status == True:
            if(Edital.objects.filter(status=True).exists()):
                raise ValidationError("Existe um edital ativo no momento.")
            return status
        else:
            return status
    
    def clean(self):
        super(EditalForm, self).clean()
        if 'data_inicio' in self.cleaned_data and 'data_final' in self.cleaned_data:
            data_inicio = self.cleaned_data['data_inicio']
            data_final = self.cleaned_data['data_final']
            if data_inicio > data_final:
                msg = "A data de Inicio não deve ser maior que a data de Término."
                self.add_error('data_inicio', msg)
           

class AlimentoNecessariosForm(forms.ModelForm):    
    class Meta:
        model = AlimentoNecessario
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AlimentoNecessariosForm, self).__init__(*args, **kwargs)
        self.fields["alimento"].queryset = Alimento.objects.all()
        self.fields["edital"].queryset = Edital.objects.filter(status=True)
        #define um template personalizado para datalist 
        self.fields["alimento"].widget.template_name = 'widgets/datalist.html'

        self.fields["alimento"].widget.attrs.update(
            {
                'style': 'text-transform: uppercase', 
                'class': 'form-control border-dark',  
                'placeholder': 'Selecione o Alimento'
            }
        )
        self.fields["edital"].widget.attrs.update({'class': 'border-dark'})
        self.fields["quantidade"].widget.attrs.update({'class': 'border-dark'})
    
class AvisosForm(forms.ModelForm):
    class Meta:
        model = Avisos
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AvisosForm, self).__init__(*args, **kwargs)
        self.fields["aviso"].widget = forms.Textarea()