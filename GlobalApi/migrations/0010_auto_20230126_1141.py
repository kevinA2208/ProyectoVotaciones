# Generated by Django 3.2.1 on 2023-01-26 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GlobalApi', '0009_auto_20230125_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lider',
            name='cantidad_votantes',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='municipios',
            name='cantidad_votantes',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='puestovotacion',
            name='cantidad_votantes',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]