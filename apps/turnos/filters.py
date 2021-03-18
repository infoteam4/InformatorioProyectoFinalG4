import django_filters
from .models import *
from django_filters import DateFilter

class turnoFilter(django_filters.FilterSet):
    class Meta:
        model = Turno
        fields = '__all__'
        exclude = ['paciente', 'estado',]

class turnoFilteradmin(django_filters.FilterSet):
    class Meta:
        model = Turno
        fields = '__all__'