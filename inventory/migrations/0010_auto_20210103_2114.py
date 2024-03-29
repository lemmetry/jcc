# Generated by Django 3.1.4 on 2021-01-03 21:14

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('fleet', '0003_auto_20210102_0346'),
        ('inventory', '0009_auto_20210103_0449'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BagOrder',
            new_name='VehicleOrder',
        ),
        migrations.RenameModel(
            old_name='BagOrderToItemAssociation',
            new_name='VehicleOrderToItemAssociation',
        ),
        migrations.AlterModelOptions(
            name='vehicleordertoitemassociation',
            options={'verbose_name': 'Vehicle Order To Item Association'},
        ),
    ]
