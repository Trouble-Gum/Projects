# Generated by Django 4.1.7 on 2023-09-21 06:40

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=martor.models.MartorField(default='Type your text here'),
        ),
    ]