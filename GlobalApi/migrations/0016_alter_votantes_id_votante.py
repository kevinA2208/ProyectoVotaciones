# Generated by Django 3.2.1 on 2023-01-26 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GlobalApi', '0015_alter_lider_doc_lider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votantes',
            name='id_votante',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
