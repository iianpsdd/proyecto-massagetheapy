from .models import *
from rest_framework import serializers

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'
        read_only_fields = ['usuario', 'fecha_reserva']  # Usuario y fecha se establecen automáticamente

    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user  # Asignar el usuario que hace la reserva
        return super().create(validated_data)


class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = '__all__'

class HistoriaClinicaSerializer(serializers.ModelSerializer):   
    class Meta:
        model = HistoriaClinica
        fields = '__all__'

class CitaServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitaServicio
        fields = '__all__'

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

