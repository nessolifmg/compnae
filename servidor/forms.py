from django import forms
from django.core.exceptions import ValidationError
from .models import Alimento, Edital, AlimentoNecessario, Avisos


class AlimentoForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Modificando os rótulos dos campos
        self.fields["nome"].label = "Nome do Alimento"

        # Adicionando classes CSS aos widgets dos campos
        self.fields["nome"].widget.attrs.update(
            {'class': 'border-dark', 'placeholder': 'Informe o nome do alimento', 'text-transform': 'uppercase'})

    def clean_nome(self):
        """
            Realiza a normalização do campo 'nome', convertendo-o para letras maiúsculas.
            Isso garante consistência nos dados independentemente do formato em que foram inseridos.
            """
        nome = self.cleaned_data["nome"]
        return nome.upper()


class EditalForm(forms.ModelForm):
    class Meta:
        model = Edital
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Modificando os rótulos dos campos
        self.fields["status"].label = "Ativar Edital"
        self.fields["data_inicio"].label = "Data de Inicio"
        self.fields["data_final"].label = "Data de Término"

        # Adicionando classes CSS aos widgets dos campos
        self.fields["numero"].widget.attrs.update(
            {'class': 'border-dark', 'placeholder': 'Ex: 2022/1'})
        self.fields["status"].widget.attrs.update(
            {'class': 'border-dark form-check-input', 'type': 'checkbox'})

        # Modificando widget
        self.fields["data_inicio"].widget = forms.DateInput(attrs={'type': 'date', 'class': 'border-dark'},
                                                            format='%Y-%m-%d')
        self.fields["data_final"].widget = forms.DateInput(attrs={'type': 'date', 'class': 'border-dark'},
                                                           format='%Y-%m-%d')

    def clean_status(self):
        """
            Realiza a validação do campo 'status' para garantir que apenas um edital esteja ativo por vez.
        """
        status = self.cleaned_data["status"]
        if status:
            if Edital.objects.filter(status=True).exclude(id=self.instance.id).exists():
                raise ValidationError("Existe um edital ativo no momento.")
            return status
        else:
            return status

    def clean(self):
        """
            Realiza a validação cruzada das datas de início e término para garantir que a data de início
            não seja posterior à data de término.
        """
        super().clean()
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
        super().__init__(*args, **kwargs)
        # Modificando os rótulos dos campos
        self.fields["edital"].widget.attrs.update(
            {'class': 'border-dark'})
        self.fields["quantidade"].widget.attrs.update(
            {'class': 'border-dark'})
        self.fields["alimento"].widget.attrs.update(
            {
                'style': 'text-transform: uppercase',
                'class': 'form-control border-dark',
                'placeholder': 'Selecione o Alimento'
            }
        )

        # define um template personalizado para datalist
        self.fields["alimento"].widget.template_name = 'widgets/datalist.html'

        # Define o conjunto de consulta (queryset) para os campos 'alimento' e 'edital'
        self.fields["alimento"].queryset = Alimento.objects.all()
        self.fields["edital"].queryset = Edital.objects.filter(status=True)


class AvisosForm(forms.ModelForm):
    class Meta:
        model = Avisos
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["aviso"].widget = forms.Textarea()
