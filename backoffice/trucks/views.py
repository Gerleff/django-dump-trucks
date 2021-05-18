"""Views of DumpTrucks app"""
import random
import re

from django.http import (HttpResponse, HttpRequest,
                         HttpResponsePermanentRedirect,
                         HttpResponseForbidden)
from django.shortcuts import render, redirect
from django.views import View

from backoffice.settings import DEBUG
from .models import Machine, Storage

from shapely import wkt


class TruckRow:
    """Truck row class for the first table"""
    def _overload(self) -> float:
        """Showing percentage of overload if needed"""
        overload = round((self.amount - self.capacity) / self.capacity * 100, 2)
        return overload if overload > 0 else 0

    def __init__(self, machine: Machine):
        self.side_number = machine.side_number
        self.model = machine.model.name
        self.capacity = machine.model.lifting_capacity
        self.amount = machine.amount
        self.overload = self._overload()


class StorageRow:
    """Storage row class for the second table"""
    def __init__(self, storage: Storage):
        self.name = storage.name
        self.prev_amount = storage.prev_amount
        self.amount = storage.amount
        self.correlation = f'{storage.silicon_dioxide}% SiO2 {storage.iron}% Fe'


class DumpTrucksView(View):
    """Main view of app"""
    def get(self, request: HttpRequest) -> HttpResponse:
        """GET request handler to give tables"""
        truck_rows = [TruckRow(machine) for machine
                      in Machine.objects.order_by('-amount', 'side_number')]
        storage_rows = [StorageRow(storage) for storage in Storage.objects.all()]
        return render(request,
                      context={'truck_rows': truck_rows,
                               'storage_rows': storage_rows},
                      template_name='trucks/landing.html')

    def _success(self, machine_pk: str) -> bool:
        """Checking out if ore transfer is successful"""
        polygon = wkt.loads(self._storage.coordinates)
        point = wkt.loads(f'POINT ({self._form_data[machine_pk]})')
        return polygon.contains(point) or polygon.covers(point)

    def _to_storage(self, machine: Machine):
        """Transferring ore to storage"""
        if self._success(machine.pk):

            _amount = self._storage.amount
            _iron = (machine.iron * machine.amount +
                     self._storage.iron * _amount) / \
                    (_amount + machine.amount)
            _silicon_dioxide = (machine.silicon_dioxide * machine.amount +
                                self._storage.silicon_dioxide * _amount) / \
                               (_amount + machine.amount)

            self._storage.iron = round(_iron, 2)
            self._storage.silicon_dioxide = round(_silicon_dioxide, 2)
            self._storage.amount += machine.amount

    def post(self, request: HttpRequest) -> HttpResponse:
        """POST request handler"""
        if _form_data := {item: request.POST[item] for item in request.POST
                          if request.POST[item] and item != 'csrfmiddlewaretoken'}:
            for item in _form_data.values():
                if not re.search(r'^[-]?[0-9]+ [-]?[0-9]+$', item):
                    return HttpResponse('Invalid coordinates inserted')
                self._form_data = _form_data
                machines = Machine.objects.filter(pk__in=self._form_data.keys())
                if len(machines):
                    self._storage = Storage.objects.first()
                    self._storage.prev_amount = self._storage.amount
                    for machine in machines:
                        self._to_storage(machine)
                        machine.amount = 0
                        machine.iron = 0
                        machine.silicon_dioxide = 0
                        machine.save()
                    self._storage.save()
        return redirect('/', permanent=True)


class ShuffleView(View):
    """View to shuffle data for better testing"""
    def post(self, request: HttpRequest) -> HttpResponse:
        if not self.request.user.is_superuser and not DEBUG:
            return HttpResponseForbidden()
        machines = Machine.objects.all()
        for machine in machines:
            machine.amount = random.randint(80, 125)
            machine.iron = round(random.randint(62, 67) / 100, 2)
            machine.silicon_dioxide = round(random.randint(30, 35) / 100, 2)
            machine.save()
        return redirect('/', permanent=True)
