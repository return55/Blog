# Generated by Django 2.1.2 on 2018-11-09 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autore', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autore',
            name='staff',
            field=models.BooleanField(default=True),
        ),
    ]
