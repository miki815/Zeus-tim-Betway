from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<int:userId>', profil, name='profil'),
    path('desetunizu/<int:userId>', deset_u_nizu, name='deset'),
    path('isplati', isplati, name='isplati'),
    path('<int:userId>/promenalozinke', promenalozinke, name='promenalozinke'),
    path('<int:userId>/brisanjenaloga', brisanjenaloga, name='brisanjenaloga'),
    path('<int:userId>/brisanjeporuka', brisanjeporuka, name='brisanjeporuka'),
    path('registracija', registracija, name='registracija'),
    path('<int:userId>/postanivip', postanivip, name='postanivip'),
    path('prikazkvotera/<int:userId>', prikaz_kvotera, name='kvoteri'),
    path('kladionica/<int:kvoterId>/<int:igracId>', prikaz_kvota, name='kvote'),
    path('kladionica/uplatitiket', uplati_tiket, name='tiket'),
    path('statistika/<int:userId>', statistika, name='statistika'),
    path('najbolji', najbolji, name='najbolji'),
    path('prikazvipkvotera/<int:userId>', prikaz_vip_kvotera, name='vipkvoteri'),
    path('vip_kladionica/<int:kvoterId>/<int:igracId>', prikaz_vip_kvota, name='vipkvote'),
]
