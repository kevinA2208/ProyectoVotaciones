# Generated by Django 3.2.1 on 2023-01-25 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GlobalApi', '0005_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='lider',
            name='cantidad_votantes',
            field=models.IntegerField(default=0),
        ),
    ]
