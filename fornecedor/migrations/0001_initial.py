# Generated by Django 4.1.10 on 2023-08-23 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('servidor', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FornecedorEdital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edital', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.PROTECT, related_name='editais_fornecedor', to='servidor.edital')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='usuarios', to='core.fornecedor')),
            ],
            options={
                'db_table': 'fornecedor_por_edital',
            },
        ),
        migrations.CreateModel(
            name='AlimentoFornecido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.FloatField(max_length=15)),
                ('alimento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='alimentos_fornecidos', to='servidor.alimento')),
                ('fornecedor_edital', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.PROTECT, related_name='fornecedores_edital', to='fornecedor.fornecedoredital')),
            ],
            options={
                'db_table': 'alimento_fornecido',
            },
        ),
    ]
