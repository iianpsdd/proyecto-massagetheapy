from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from . import views
from .views import registrar_usuario

router = DefaultRouter()
router.register(r'usuario', views.UsuarioViewSet)
router.register(r'servicio', views.ServicioViewSet)
router.register(r'cita', views.CitaViewSet)
router.register(r'historiaclinica', views.HistoriaClinicaViewSet)
router.register(r'citaservicio', views.CitaServicioViewSet)
router.register(r'reserva', views.ReservaViewSet)


urlpatterns = [
#____________________Url de la api_________________________________

    path("api/1.0/", include(router.urls)),

#____________________Otras Urls___________________________________
    path("recuperar_clave_form/", views.recuperar_clave_form, name="recuperar_clave_form"),
    path("olvide_mi_clave/<str:email>/", views.olvide_mi_clave, name="olvide_mi_clave"),
	path("verificar_token_form/<str:email>/", views.verificar_token_form, name="verificar_token_form"),
	path("cambiar_clave/", views.cambiar_clave, name="cambiar_clave"),



#____________________Inicio y cierre de seccion_________________________________
    path('', views.index, name='index'),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path('inicio', views.inicio, name='inicio'),

#____________________Modulo usuario_________________________________

    path('registrar/', registrar_usuario, name='registrar_usuario'),
    path('registrarAdmin/', views.registrarAdmin, name='registrarAdmin'),
    path("registrarUsuario/", views.registrarUsuario, name="registrarUsuario"),
    path("registrarUsuario2/", views.registrarUsuario2, name="registrarUsuario2"),
    path('buscarUsuario/', views.buscarUsuario, name='buscarUsuario'),
    path("registrar_usuario_manual/", views.registrar_usuario_manual, name="registrar_usuario_manual"),
    path("usuario_editar/<int:id_Usuario>/", views.usuario_editar, name="usuario_editar"),
    path("usuario_actualizar/", views.usuario_actualizar, name="usuario_actualizar"),
    path('usuario/eliminar/<int:id_usuario>/', views.eliminar_usuario, name='eliminar_usuario'),
    path("buscar/", views.buscar, name="buscar"),

#____________________Modulo historia clinica_________________________________

    path('buscarHistoriaClinica/', views.buscarHistoriaClinica, name='buscarHistoriaClinica'),
    # path('historiaClinica/', views.historiaClinica, name='historiaClinica'),
    path('crearHistoriaClinica/<str:identificacion>/', views.crear_historia_clinica, name='crearHistoriaClinica'),
    path('buscar-identificacion/', views.buscar_identificacion, name='buscarIdentificacion'),
    

#____________________Modulo Servicios_________________________________________
    path('registrarServicio/', views.registrarServicio, name='registrarServicio'),
    # path('buscarServicio/', views.buscarServicio, name='buscarServicio'),
    path('servicios/', views.servicios, name='servicios'),
    path('buscarServicio/', views.servicios, name='buscarServicio'),
    path('eliminarServicio/<int:id>/', views.eliminarServicio, name='eleliminarServicio'),
    path('editarServicio/<int:id>/', views.editarServicio, name='editarServicio'),
    path('actualizarServicio/<int:id>/', views.actualizarServicio, name='actualizarServicio'),
    path("busquedaServicio/", views.busquedaServicio, name="busquedaServicio"),
    path('usuarios_especialistas/', views.obtener_especialistas, name='usuarios_especialistas'),
#____________________Modulo reservas_________________________________________

    path('buscar_usuarioSecre/', views.buscar_usuarioSecre, name='buscar_usuarioSecre'),
    path('crear_reserva_secre/', views.crear_reserva_secre, name='crear_reserva_secre'),
    # path('reservas/', views.listar_reservas, name='reservas'),
    path('creareserva/', views.crear_reserva, name='crear_reserva'),
    path('listar_reservas/', views.listar_reservas, name='listar_reservas'),
    path('cancelar_reserva/', views.cancelar_reserva, name='cancelar_reserva'),    
    path('reservas/', views.servicios, name='reservas'),
    path('misReservas/', views.misReservas, name='misReservas'),  
    path('confirmar_reserva/', views.confirmar_reserva, name='confirmar_reserva'),      
#__________________urls de prueva del calendario_____________________________

    path('calendario/', views.calendario, name='calendario'),
    path('all_events/', views.all_events, name='all_events'),
    path('add_event/', views.add_event, name='add_event'),
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),

]
