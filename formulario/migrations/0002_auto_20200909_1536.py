# Generated by Django 3.1.1 on 2020-09-09 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulario', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mapeamento',
            name='status',
        ),
        migrations.AddField(
            model_name='mapeamento',
            name='is_online',
            field=models.IntegerField(choices=[(1, 'Sim'), (2, 'Não'), (3, 'Sem confirmação')], default=3),
        ),
    ]
