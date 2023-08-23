# Generated by Django 4.1.10 on 2023-08-23 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('cpf_cnpj', models.CharField(max_length=14)),
                ('telefone', models.CharField(max_length=15)),
                ('cidade', models.CharField(max_length=150)),
                ('estado', models.CharField(max_length=2)),
                ('endereco', models.CharField(max_length=150)),
                ('bairro', models.CharField(max_length=150)),
                ('nascimento', models.DateField()),
                ('dap', models.CharField(max_length=25)),
                ('associacao', models.CharField(blank=True, max_length=15)),
                ('prioritario', models.CharField(choices=[('1', 'Quilombola'), ('2', 'Indígena'), ('3', 'Nenhum')], default='3', max_length=1)),
            ],
            options={
                'db_table': 'fornecedor',
            },
        ),
    ]
