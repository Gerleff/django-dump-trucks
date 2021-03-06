"""Generated by Django 3.2 on 2021-05-18 02:38"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    """Initial migration"""
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('prev_amount', models.FloatField(help_text='в тоннах',
                                                  verbose_name='Предыдущая заполненность')),
                ('amount', models.FloatField(help_text='в тоннах',
                                             verbose_name='Текущая заполненность')),
                ('silicon_dioxide', models.FloatField(help_text='в процентах',
                                                      null=True, verbose_name='SiO2')),
                ('iron', models.FloatField(help_text='в процентах',
                                           null=True, verbose_name='Fe')),
                ('coordinates', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'storages',
            },
        ),
        migrations.CreateModel(
            name='TruckModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True,
                                          verbose_name='Название')),
                ('lifting_capacity', models.FloatField(verbose_name='Грузоподъемность ')),
            ],
            options={
                'db_table': 'models',
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('side_number', models.CharField(max_length=64, primary_key=True,
                                                 serialize=False, verbose_name='Номер борта')),
                ('amount', models.FloatField(help_text='в тоннах',
                                             verbose_name='Перевозимый груз')),
                ('silicon_dioxide', models.FloatField(help_text='в процентах',
                                                      null=True, verbose_name='SiO2')),
                ('iron', models.FloatField(help_text='в процентах',
                                           null=True, verbose_name='Fe')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            to='trucks.truckmodel', verbose_name='Модель')),
            ],
            options={
                'db_table': 'machines',
            },
        ),
    ]
