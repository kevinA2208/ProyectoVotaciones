# Generated by Django 3.2.1 on 2023-01-26 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GlobalApi', '0010_auto_20230126_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='doc',
            field=models.CharField(editable=False, max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='Numero de documento'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, editable=False, max_length=50, null=True, verbose_name='Nombre de usuario'),
        ),
    ]
