# Generated by Django 2.1.2 on 2018-11-04 16:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Autore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('data_registrazione', models.DateField(default=datetime.date.today, editable=False)),
                ('bio', models.TextField(blank=True)),
                ('profilo_pubblico', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Autori',
                'get_latest_by': ['first_name', 'last_name'],
            },
        ),
    ]
