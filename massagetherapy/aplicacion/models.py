from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages



class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    password = models.CharField(max_length=254)
    DOCUMENTOS = (
        ("TI", "Tarjera de identidad"),
        ("CC", "Cedula"),
        ("PA", "Pasaporte"),
        ("CE", "Cedula extrangeria"),
    )
    tipo_documento = models.CharField(max_length=2, choices=DOCUMENTOS, null=False, blank=False)
    username = models.CharField(max_length=50) # identificacion
    foto = models.ImageField(upload_to="fotos/", default="fotos/default.png")
    ROLES = (
        ("ADMIN", "Administrador"),
        ("SECRE", "Secretaria"),
        ("ESPEC", "Especialista"),
        ("USUAR", "Usuario"),
    )
    rol = models.CharField(max_length=5, choices=ROLES, default="USUAR", null=True, blank=True)
    email = models.EmailField(max_length=254, default="iianpsdd@gmail.com", unique=True)
    token = models.CharField(max_length=10, null=True, blank=True)
    telefono = models.CharField(max_length=15, blank=True, null=True, default='')
    fecha_nacimiento = models.DateField()

    def clean(self):
        super().clean()
        if self.fecha_nacimiento > timezone.now().date():
            raise ValidationError('La fecha de nacimiento no puede ser futura.')
        
    def save(self, *args, **kwargs):
        # Verificar si el usuario es el ADMIN predeterminado
        if self.pk:  # Si el usuario ya existe en la base de datos
            original = Usuario.objects.get(pk=self.pk)
            if (
                original.rol == "ADMIN" 
                and original.username == "admin_predeterminado"
            ):
                # Comparar campos modificados
                if (
                    self.nombre != original.nombre 
                    or self.apellido != original.apellido 
                    or self.password != original.password 
                    or self.tipo_documento != original.tipo_documento 
                    or self.username != original.username 
                    or self.foto != original.foto 
                    or self.email != original.email 
                    or self.telefono != original.telefono 
                    or self.fecha_nacimiento != original.fecha_nacimiento
                ):
                    raise ValidationError("No se puede modificar al administrador predeterminado.")
        super().save(*args, **kwargs)        
        
    def delete(self, *args, **kwargs):
        # Verificar si el usuario es el ADMIN predeterminado
        if self.rol == "ADMIN" and self.username == "admin_predeterminado":
            raise ValidationError("No se puede eliminar al administrador predeterminado.")
        # Verificar si el usuario es un ESPEC y ha creado historias clínicas
        if self.rol == "ESPEC" and HistoriaClinica.objects.filter(especialista=self).exists():
            raise ValidationError("Lo sentimos, pero no se puede eliminar a este especialista porque tiene historias clínicas asociadas.")
        super().delete(*args, **kwargs)        

    def __str__(self):
        return f"{self.nombre} {self.apellido} {self.username}"


class Servicio(models.Model):
    nombreServicio = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    nombreEspecialista = models.CharField(max_length=100)

    def __str__(self):
        return self.nombreServicio

class Reserva(models.Model):
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    fecha = models.DateField(null=True)  # Campo separado para la fecha
    hora = models.CharField(max_length=10, null=True)  # Campo separado para la hora
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    ESTADOS = (
        ("P", "Pendiente"),
        ("A", "Atendida"),
        ("N", "No atendida"),
        ("C", "Cancelada"),
    )
    estado = models.CharField(max_length=1, choices=ESTADOS, default="P")
    usuario_cancelacion = models.CharField(max_length=150, null=True, blank=True)  # Nuevo campo

    class Meta:
        unique_together = ('servicio', 'fecha', 'hora')  # Ahora son únicos juntos

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.servicio.nombreServicio} en {self.fecha} a las {self.hora}"



class Cita(models.Model):
    idUsuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idServicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    repeticiones = models.IntegerField()
    ESTADOS = (
        ("P", "Pendiente"),
        ("C", "Cancelada"), 
        ("A", "Admitida"),
    )
    estado = models.CharField(max_length=1, choices=ESTADOS, default="P")

    def __str__(self):
        return self.estado


class HistoriaClinica(models.Model):
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='paciente_historia')
    especialista = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='especialista_historia')
    evolucion = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    observaciones = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    reserva_id = models.IntegerField(null=True, blank=True)  # Nuevo campo para almacenar el ID de la reserva
    fecha_reserva = models.DateField(null=True, blank=True)  # Nuevo campo para almacenar la fecha de la reserva

class CitaServicio(models.Model):
    idUsuarioServicio = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    idServicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

"""__________________________tablas de calendario mejoras futuras_________________________________________"""

class Events(models.Model):
    name = models.CharField(max_length=254, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)



