# Generated by Django 4.1.7 on 2023-03-16 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logserver', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machinegroup',
            name='machines',
        ),
        migrations.RemoveField(
            model_name='machinegroup',
            name='users',
        ),
        migrations.RemoveField(
            model_name='policy',
            name='mgroup',
        ),
    ]