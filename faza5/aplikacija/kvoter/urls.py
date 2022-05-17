from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<int:userId>/napravikvote', napravikvote, name='napravikvote'),
    path('<int:userId>/prikaziaktivneutakmice', prikaziaktivneutakmice, name='prikaziaktivneutakmice'),


]
