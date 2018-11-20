# Generated by Django 2.1.2 on 2018-11-19 17:44

import articolo.models
import datetime
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articolo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titolo', models.CharField(help_text='Titolo', max_length=200, unique=True)),
                ('testo', models.TextField()),
                ('data', models.DateField(default=datetime.date.today, editable=False)),
                ('keywords', django.contrib.postgres.fields.ArrayField(base_field=articolo.models.LowerCaseCharField(max_length=15), blank=True, default=list, help_text='Puoi inserire max 10 parole chiave per il tuo articolo', size=10)),
                ('categoria', models.CharField(choices=[('CINEMA', 'Cinema'), ('SCIENZA', 'Scienza'), ('SPORT', 'Sport'), ('CUCINA', 'Cucina'), ('POLITICA', 'Politica'), ('VIAGGI', 'Viaggi')], help_text='Categoria', max_length=8)),
                ('citato', models.IntegerField(default=0, editable=False)),
                ('somma_voti', models.IntegerField(default=0, editable=False)),
                ('numero_voti', models.IntegerField(default=0, editable=False)),
                ('cita', models.ManyToManyField(blank=True, to='articolo.Articolo')),
                ('id_autore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Articoli',
                'get_latest_by': '-data',
            },
        ),
        migrations.CreateModel(
            name='Commento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testo', models.TextField()),
                ('data', models.DateField(default=datetime.date.today, editable=False)),
                ('commentatore', models.CharField(default='Anonimo', help_text='Nick name', max_length=15)),
                ('id_articolo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articolo.Articolo')),
            ],
            options={
                'verbose_name_plural': 'Commenti',
            },
        ),
        migrations.AlterUniqueTogether(
            name='commento',
            unique_together={('id_articolo', 'id')},
        ),
    ]
