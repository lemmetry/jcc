# Generated by Django 3.2.15 on 2022-12-10 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0004_alter_station_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='station_id',
        ),
    ]
