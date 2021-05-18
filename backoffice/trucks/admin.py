"""Trucks admin models"""
from django.contrib import admin
from .models import Machine, Storage, TruckModel


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    """Machine admin model"""
    list_display = ('side_number', 'model', 'amount', 'silicon_dioxide', 'iron')
    list_editable = ('amount', 'silicon_dioxide', 'iron')


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    """Storage admin model"""
    list_display = ('name', 'amount', 'silicon_dioxide', 'iron', 'coordinates')
    list_editable = ('amount', 'silicon_dioxide', 'iron')


@admin.register(TruckModel)
class TruckModelAdmin(admin.ModelAdmin):
    """TruckModel admin model"""
    list_display = ('name', 'lifting_capacity')
