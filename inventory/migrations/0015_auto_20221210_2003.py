# Generated by Django 3.2.15 on 2022-12-10 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_auto_20210108_2136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bagcompartment',
            options={'ordering': ['ordering']},
        ),
        migrations.RemoveField(
            model_name='vehicleorder',
            name='timestamp',
        ),
    ]
