from django import forms
from .models import *

class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = HistoriaClinica
        fields = ['evolucion', 'diagnostico', 'tratamiento', 'observaciones']


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombreServicio', 'descripcion', 'nombreEspecialista', 'precio']