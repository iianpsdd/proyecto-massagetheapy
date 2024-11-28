from django.contrib import admin, messages
from .models import *
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido', 'tipo_documento', 'username', 'rol', 'fecha_nacimiento', 'email', 'ver_foto']
    
    def ver_foto(self, obj):
        if obj.foto:
            return mark_safe(f"<img src='{obj.foto.url}' width='20%' />")
        return "No image"
    
    def delete_model(self, request, obj):
        try:
            obj.delete()
        except ValidationError as e:
            # Mostrar el mensaje como advertencia
            self.message_user(request, str(e), level=messages.ERROR)
    
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            try:
                obj.delete()
            except ValidationError as e:
                self.message_user(request, str(e), level=messages.ERROR)

admin.site.register(Usuario, UsuarioAdmin)

class ServicioAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombreServicio', 'precio', 'descripcion', 'nombreEspecialista']

admin.site.register(Servicio, ServicioAdmin)

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'servicio', 'usuario', 'fecha', 'hora', 'estado', 'usuario_cancelacion')
    list_filter = ('estado', 'fecha')
    search_fields = ('usuario__username', 'servicio__nombreServicio')
    ordering = ('-fecha',)
    fields = ('servicio', 'usuario', 'fecha', 'hora', 'estado', 'usuario_cancelacion')
    readonly_fields = ('usuario_cancelacion',)

    def save_model(self, request, obj, form, change):
        if 'estado' in form.changed_data:
            if obj.estado == 'C':
                obj.usuario_cancelacion = request.user.username
        super().save_model(request, obj, form, change)

admin.site.register(Reserva, ReservaAdmin)



class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ['id', 'evolucion', 'diagnostico', 'tratamiento', 'observaciones']

admin.site.register(HistoriaClinica, HistoriaClinicaAdmin)

class CitaServicioClinicaAdmin(admin.ModelAdmin):
    list_display = ['id', 'idUsuarioServicio', 'idServicio', 'precio']

admin.site.register(CitaServicio, CitaServicioClinicaAdmin)

class EventsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'start', 'end']

admin.site.register(Events, EventsAdmin)


# # Registra los modelos sin duplicados
# admin.site.register(Servicio, ServicioAdmin)  # Registra Servicio solo una vez
# admin.site.register(Reserva, ReservaAdmin)
# admin.site.register(Cita, CitaAdmin)
# admin.site.register(HistoriaClinica, HistoriaClinicaAdmin)
# admin.site.register(CitaServicio, CitaServicioClinicaAdmin)
# admin.site.register(Events, EventsAdmin)
