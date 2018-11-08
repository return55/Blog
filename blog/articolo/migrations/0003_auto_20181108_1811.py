# Generated by Django 2.1.2 on 2018-11-08 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articolo', '0002_auto_20181106_2343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articolo',
            old_name='citazioni',
            new_name='cita',
        ),
        migrations.AddField(
            model_name='articolo',
            name='citato',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='commento',
            name='commentatore',
            field=models.CharField(default='Anonimo', help_text='Nick name', max_length=15),
        ),
    ]