# Generated by Django 3.0.1 on 2019-12-25 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('brand', models.CharField(blank=True, max_length=40, null=True)),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Compartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('brand', models.CharField(blank=True, max_length=40, null=True)),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('notes', models.CharField(blank=True, max_length=60)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('brand', models.CharField(blank=True, max_length=40, null=True)),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('size', models.CharField(blank=True, max_length=40)),
                ('notes', models.CharField(blank=True, max_length=60)),
                ('supplied_by', models.CharField(choices=[('HOSPITAL', 'Hospital'), ('EMS_COMS', 'EMS Coms')], default='HOSPITAL', max_length=10)),
            ],
            options={
                'ordering': ['name', 'size'],
            },
        ),
        migrations.CreateModel(
            name='Kit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('brand', models.CharField(blank=True, max_length=40, null=True)),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KitItemAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Item')),
                ('kit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Kit')),
            ],
            options={
                'verbose_name': 'Kit-Item Association',
                'verbose_name_plural': 'Kit-Item Association',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='KitCompartmentAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('compartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Compartment')),
                ('kit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Kit')),
            ],
            options={
                'verbose_name': 'Kit-Compartment Association',
                'verbose_name_plural': 'Kit-Compartment Association',
                'ordering': ['ordering'],
            },
        ),
        migrations.AddField(
            model_name='kit',
            name='items',
            field=models.ManyToManyField(through='inventory.KitItemAssociation', to='inventory.Item'),
        ),
        migrations.CreateModel(
            name='CompartmentKitAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('compartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Compartment')),
                ('kit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Kit')),
            ],
            options={
                'verbose_name': 'Compartment-Kit Association',
                'verbose_name_plural': 'Compartment-Kits Association',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='CompartmentItemAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('compartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Compartment')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Item')),
            ],
            options={
                'verbose_name': 'Compartment-Item Association',
                'verbose_name_plural': 'Compartment-Items Association',
                'ordering': ['ordering'],
            },
        ),
        migrations.AddField(
            model_name='compartment',
            name='items',
            field=models.ManyToManyField(through='inventory.CompartmentItemAssociation', to='inventory.Item'),
        ),
        migrations.AddField(
            model_name='compartment',
            name='kits',
            field=models.ManyToManyField(blank=True, through='inventory.CompartmentKitAssociation', to='inventory.Kit'),
        ),
        migrations.CreateModel(
            name='BagCompartmentAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('bag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Bag')),
                ('compartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Compartment')),
            ],
            options={
                'verbose_name': 'Bag-Compartment Association',
                'verbose_name_plural': 'Bag-Compartment Associations',
                'ordering': ['ordering'],
            },
        ),
        migrations.AddField(
            model_name='bag',
            name='compartments',
            field=models.ManyToManyField(through='inventory.BagCompartmentAssociation', to='inventory.Compartment'),
        ),
    ]