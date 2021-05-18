"""URL-settings"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path

from trucks.views import DumpTrucksView, ShuffleView


def ping(request):
    """Ping!"""
    return HttpResponse('pong')


urlpatterns = [
    path('ping', ping),
    path('', DumpTrucksView.as_view()),
    path('shuffle', ShuffleView.as_view()),
    path('admin/', admin.site.urls)
]
