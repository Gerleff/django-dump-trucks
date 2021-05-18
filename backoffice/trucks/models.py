"""Description of DumpTrucks app's models"""
from django.db import models


class TruckModel(models.Model):
    """Truck model model"""
    name = models.CharField('Название', max_length=64, unique=True)
    lifting_capacity = models.FloatField('Грузоподъемность ')

    def __str__(self):
        """String representation"""
        return self.name

    class Meta:
        """Meta-data"""
        db_table = 'models'


class Machine(models.Model):
    """Machine model"""
    side_number = models.CharField('Номер борта', max_length=64, primary_key=True)
    model = models.ForeignKey(TruckModel, verbose_name='Модель',
                              on_delete=models.CASCADE)
    amount = models.FloatField('Перевозимый груз', help_text='в тоннах')
    silicon_dioxide = models.FloatField('SiO2', null=True, help_text='в процентах')
    iron = models.FloatField('Fe', null=True, help_text='в процентах')

    def __str__(self):
        """String representation"""
        return f'{self.model.name} №{self.side_number}'

    class Meta:
        """Meta-data"""
        db_table = 'machines'


class Storage(models.Model):
    """Storage model"""
    name = models.CharField('Название', max_length=64)
    prev_amount = models.FloatField('Предыдущая заполненность', help_text='в тоннах')
    amount = models.FloatField('Текущая заполненность', help_text='в тоннах')
    silicon_dioxide = models.FloatField('SiO2', null=True, help_text='в процентах')
    iron = models.FloatField('Fe', null=True, help_text='в процентах')
    coordinates = models.CharField(max_length=64)

    def __str__(self):
        """String representation"""
        return self.name

    class Meta:
        """Meta-data"""
        db_table = 'storages'
