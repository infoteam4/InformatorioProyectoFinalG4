"""proyectoinfoG4v2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from apps.turnos.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = 'home'),
    path('paciente/', paciente, name = 'paciente'),
    path('login/', loginPaciente, name = 'login'),
    path('logout/', logoutPaciente, name = 'logout'),
    path('registro/', registro, name = 'registro'),
    path('eliminacion/<int:pk>', cancelarTurno, name = 'cancelarTurno'),
    path('elegirservicio/', elegirServicio, name = 'elegirServicio'),
    path('sacarturno/<int:pk>/', sacarTurno, name = 'sacarTurno'),
    path('turnoconfirmado/<int:pk>/', turnoConfirmado, name = 'turnoConfirmado'),
    path('misdatos/', misDatos, name = 'misdatos'),
    path('modifServicio/<int:pk>/', modifServicio, name = 'modifServicio'),
    path('modifTurno/<int:pk>/', modifTurno, name = 'modifTurno'),
    path('turnoModificado/<int:pk>/', turnoModificado, name = 'turnoModificado'),
    path('crearservicio/', altaServicio, name = 'altaServicio'),
    path('crearpractica/', altaPractica, name = 'altaPractica'),
    path('modificarnovedades/', modifNovedades, name = 'modificarnovedades'),
    
]
