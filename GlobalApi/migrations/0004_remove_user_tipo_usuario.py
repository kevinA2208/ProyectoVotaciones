# Generated by Django 3.2.1 on 2023-01-25 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GlobalApi', '0003_remove_user_foto_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='tipo_usuario',
        ),
    ]
