# Generated by Django 3.2.1 on 2023-01-25 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GlobalApi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tipo_usuario',
            field=models.CharField(default=1, max_length=1, verbose_name='Tipo de usuario'),
            preserve_default=False,
        ),
    ]
