# Generated by Django 4.1.10 on 2023-08-23 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=15, unique=True)),
            ],
            options={
                'db_table': 'alimento',
            },
        ),
        migrations.CreateModel(
            name='Avisos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aviso', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'db_table': 'avisos',
            },
        ),
        migrations.CreateModel(
            name='Edital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=15, unique=True)),
                ('status', models.BooleanField(blank=True, default=False)),
                ('data_inicio', models.DateField()),
                ('data_final', models.DateField()),
            ],
            options={
                'db_table': 'edital',
            },
        ),
        migrations.CreateModel(
            name='AlimentoNecessario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.FloatField(max_length=15)),
                ('alimento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='alimentos_necessarios', to='servidor.alimento')),
                ('edital', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.PROTECT, related_name='editais_alimentos', to='servidor.edital')),
            ],
            options={
                'db_table': 'alimento_necessario',
            },
        ),
    ]
