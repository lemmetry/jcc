# Generated by Django 3.1.4 on 2020-12-25 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20201225_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bagcompartment',
            name='items',
        ),
        migrations.RemoveField(
            model_name='kit',
            name='items',
        ),
        migrations.RemoveField(
            model_name='kitcompartment',
            name='items',
        ),
        migrations.CreateModel(
            name='KitToItemAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
                ('kit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.kit')),
            ],
        ),
        migrations.CreateModel(
            name='KitCompartmentToItemAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
                ('kit_compartment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.kitcompartment')),
            ],
        ),
        migrations.CreateModel(
            name='BagCompartmentToItemAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('bag_compartment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.bagcompartment')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
            ],
        ),
    ]
