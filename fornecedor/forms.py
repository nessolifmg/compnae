from django import forms as django_forms
from .models import AlimentoFornecido


class FornecerAlimentosForm(django_forms.ModelForm):
    class Meta:
        model = AlimentoFornecido
        fields = "__all__"
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
