from random import randint
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import *
from django.http import JsonResponse
from django.db import IntegrityError, transaction
from .models import Usuario, Servicio, Reserva
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
import json
import requests
import re
from .utils import role_required
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import check_password, make_password
from os import path




from .serializers import *
from rest_framework import viewsets

from django.db.models import Q, Count
from django.conf import settings
from .encriptar import *
from django.shortcuts import render, get_object_or_404, redirect
from .forms import HistoriaClinicaForm



@receiver(post_migrate)
def crear_admin_predeterminado(sender, **kwargs):
    # Verifica si ya existe un ADMIN predeterminado
    if not Usuario.objects.filter(username="admin_predeterminado").exists():
        # Encriptar la contraseña antes de crear el usuario
        password_encriptada = hash_password("admin12345")  

        Usuario.objects.create(
            nombre="Admin",
            apellido="Predeterminado",
            password=password_encriptada,  
            tipo_documento="CC",
            username="admin_predeterminado",
            email="admin@example.com",
            rol="ADMIN",
            fecha_nacimiento="2000-01-01"
        )

def index(request):
    logueo = request.session.get("logueo", False)
    if logueo:
        return render(request, './inicio.html', {})
    else:
        return render(request, './index.html', {})


def inicio(request):
    logueo = request.session.get("logueo", False)
    if logueo:
        return render(request, './inicio.html', {})
    else:
        return redirect("index")


def index2(request):
    return HttpResponse("Bienvenido a django=rest")


def login(request):
    if request.method == "POST":
        identificacion = request.POST.get("identification")
        password = request.POST.get("clave")
        try:
            q = Usuario.objects.get(username=identificacion)
            verify = verify_password(password, q.password)
            if verify:
                # Si no hay foto asignada, usa la imagen por defecto
                foto_url = q.foto.url if q.foto else '/aplicacion/static/img/perfil.jpg'
                request.session["logueo"] = {
                    "id": q.id,
                    "nombre": q.nombre,
                    "rol": q.rol,
                    "foto": foto_url,
                    "username": q.username,
                }

                next_url = request.POST.get('next', reverse('reservas'))  # Redirigir a 'reservas' si no hay 'next'
                return JsonResponse({'success': True, 'next': next_url})
            else:
                return JsonResponse({'success': False, 'message': 'Contraseña incorrecta', 'tipo': 'danger'})
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Datos incorrectos', 'tipo': 'danger'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e), 'tipo': 'danger'})
    else:
        return JsonResponse({'success': False, 'message': 'No se enviaron datos...', 'tipo': 'danger'})



def logout(request):
    logueo = request.session.get("logueo", False)
    print(logueo)
    if logueo:
        del request.session["logueo"]
        # del request.session["carrito"]
        return redirect("index")
    else:
        messages.info(request, "No se pudo cerrar sesión, intente de nuevo")
        return redirect("inicio")


def handle_uploaded_file(f):
    with open(f"{settings.MEDIA_ROOT}/fotos/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@role_required(["ADMIN"])
def registrarAdmin(request):  # Registro de admin
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        identificacion = request.POST.get("identificacion")
        tipoIdentificacion = request.POST.get("tipoIdentificacion")
        rol = request.POST.get("rol")
        clave1 = request.POST.get("clave1")
        clave2 = request.POST.get("clave2")
        foto = request.FILES.get("foto")
        fecha_nacimiento = request.POST.get("fecha_nacimiento")  

        #  lista para almacenar los errores
        errores = []

        if foto:
            extension = os.path.splitext(foto.name)[1].lower()
            if extension not in ['.jpg', '.jpeg', '.png']:
                errores.append('El archivo de la foto debe ser de tipo JPG o PNG.')
            else:
                foto_url = foto
        else:
            foto_url = "fotos/default.png"

        # Verificar si el correo ya existe
        if not errores and Usuario.objects.filter(email=correo).exists():
            errores.append('Ya existe una cuenta con ese correo. Intente con uno diferente.')

        # Verificar si el username ya existe
        if not errores and Usuario.objects.filter(username=identificacion).exists():
            errores.append('Ya existe una cuenta con esa identificación. Intente con una diferente.')

        # Validaciones de identificación
        if not errores and not identificacion.isdigit():
            errores.append('La identificación debe contener solo números.')
        elif not errores and (len(identificacion) > 10 or len(identificacion) < 5):
            errores.append('La identificación debe tener entre 5 y 10 dígitos.')

        # Verificar que las contraseñas coinciden
        if not errores and clave1 != clave2:
            errores.append('Las contraseñas no coinciden. Por favor verifícalas.')

        # Validar la fecha de nacimiento
        if not errores and fecha_nacimiento:
            try:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
                if fecha_nacimiento > timezone.now().date():
                    errores.append('La fecha de nacimiento no puede ser futura.')
            except ValueError:
                errores.append('La fecha de nacimiento no es válida.')

        # Validar la edad y el tipo de identificación (si no hay errores previos)
        if not errores and fecha_nacimiento:
            edad = (timezone.now().date() - fecha_nacimiento).days // 365  # Cálculo de la edad en años

            # Si es menor de 18 años
            if edad < 18 and tipoIdentificacion != "Tarjeta de Identidad":
                errores.append('Si eres menor de 18 años, debes seleccionar "Tarjeta de Identidad".')

            # Si es mayor de 18 años
            if edad >= 18 and tipoIdentificacion == "Tarjeta de Identidad":
                errores.append('Si eres mayor de 18 años, debes seleccionar "Cédula de Ciudadanía", "Pasaporte" o "Cédula de Extranjería".')


        # Si hay errores, se retornan los mensajes de error
        if errores:
            for error in errores:
                messages.error(request, error)
            return render(request, "usuarios/registrarUsuario2.html", {
                "nombre": nombre,
                "apellido": apellido,
                "correo": correo,
                "identificacion": identificacion,
                "tipoIdentificacion": tipoIdentificacion,
                "rol": rol,
                "foto": foto,
                "fecha_nacimiento": fecha_nacimiento,
            }) 

        clave = hash_password(clave1)

        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=correo,
            username=identificacion,
            tipo_documento=tipoIdentificacion,
            rol=rol,
            password=clave,
            foto=foto_url,
            fecha_nacimiento=fecha_nacimiento, 
        )
        usuario.save()

        messages.success(request, 'Registro exitoso.')
        return redirect("registrarUsuario2")
    
    messages.error(request, 'Ocurrió un error en el servidor. Intente nuevamente más tarde.')
    return redirect("registrarUsuario2")

# Registro del index
def registrar_usuario_manual(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        identificacion = request.POST.get("identificacion")
        tipoIdentificacion = request.POST.get("tipoIdentificacion")
        rol = request.POST.get("rol")
        clave1 = request.POST.get("clave1")
        clave2 = request.POST.get("clave2")
        foto = request.FILES.get("foto")
        fecha_nacimiento = request.POST.get("fecha_nacimiento")

        #  lista para almacenar los errores
        errores = []

        if foto:
            extension = os.path.splitext(foto.name)[1].lower()
            if extension not in ['.jpg', '.jpeg', '.png']:
                errores.append('El archivo de la foto debe ser de tipo JPG o PNG.')
            else:
                foto_url = foto
        else:
            foto_url = "fotos/default.png"

        # Verificar si el correo ya existe
        if not errores and Usuario.objects.filter(email=correo).exists():
            errores.append('Ya existe una cuenta con ese correo. Intente con uno diferente.')

        # Verificar si el username ya existe
        if not errores and Usuario.objects.filter(username=identificacion).exists():
            errores.append('Ya existe una cuenta con esa identificación. Intente con una diferente.')

        # Validaciones de identificación
        if not errores and not identificacion.isdigit():
            errores.append('La identificación debe contener solo números.')
        elif not errores and (len(identificacion) > 10 or len(identificacion) < 5):
            errores.append('La identificación debe tener entre 5 y 10 dígitos.')

        # Verificar que las contraseñas coinciden
        if not errores and clave1 != clave2:
            errores.append('Las contraseñas no coinciden. Por favor verifícalas.')

        # Validar la fecha de nacimiento
        if not errores and fecha_nacimiento:
            try:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
                if fecha_nacimiento > timezone.now().date():
                    errores.append('La fecha de nacimiento no puede ser futura.')
            except ValueError:
                errores.append('La fecha de nacimiento no es válida.')

        if errores:
            for error in errores:
                messages.error(request, error)
            return render(request, "usuarios/registrarUsuario.html", {
                "nombre": nombre,
                "apellido": apellido,
                "correo": correo,
                "identificacion": identificacion,
                "tipoIdentificacion": tipoIdentificacion,
                "rol": rol,
                "clave2": clave2,
                "clave1": clave1,
                "foto": foto,
                "fecha_nacimiento": fecha_nacimiento,
            })  

        clave = hash_password(clave1)

        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=correo,
            username=identificacion,
            tipo_documento=tipoIdentificacion,
            rol=rol,
            password=clave,  
            foto=foto_url,
            fecha_nacimiento=fecha_nacimiento,  
        )
        usuario.save()

        # Guarda los datos en la sesión para el usuario registrado
        request.session["logueo"] = {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "rol": usuario.rol,
            "foto": usuario.foto.url,
            "username": usuario.username,
        }

        messages.success(request, '¡Registro exitoso! ')
        messages.success(request, '¡Bienvenido!')
        return redirect("inicio") 

    return render(request, "usuarios/registrarUsuario.html")




############################################################################
def registrar_usuario(request):
    if request.method == "POST":
        correo = request.POST.get("email")

        # Verificar si el correo ya existe
        if Usuario.objects.filter(email=correo).exists():
            # Si el correo ya está registrado, devolver un mensaje de error
            return JsonResponse({'error': 'El correo ya está en uso.'}, status=400)
        return JsonResponse({'success': True}, status=200)
    return render(request, 'registrarUsuario.html')

####################################################################################
def buscar(request):
    if request.method == "POST":
        dato = request.POST.get("dato_buscar", '').strip()
        rol_filtrar = request.POST.get("rol_filtrar", '').strip()

        q = Usuario.objects.all()

        # Filtrar por nombre o apellido
        if dato:
            q = q.filter(Q(nombre__icontains=dato) | Q(apellido__icontains=dato) | Q(username__icontains=dato) | Q(tipo_documento__icontains=dato))

        if rol_filtrar:
            q = q.filter(rol=rol_filtrar)

        # Diccionario de roles a alias
        roles_alias = {
            'ADMIN': 'Administrador',
            'SECRE': 'Secretaria',
            'ESPEC': 'Especialista',
            'USUAR': 'Cliente'
        }
        usuarios_con_alias = []
        for usuario in q:
            usuarios_con_alias.append({
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'tipo_documento': usuario.tipo_documento,
                'username': usuario.username,
                'rol_alias': roles_alias.get(usuario.rol, usuario.rol) 
            })

        contexto = {"data": usuarios_con_alias}
        return render(request, "usuarios/buscarUsuario.html", contexto)
    else:
        messages.warning(request, "No se enviaron datos...")
        return redirect("buscarUsuario")
#---------------------------------------------------------------------------------------------------

def crear_reserva_auxiliar(servicio_id, fecha, hora_str, usuario):
    try:
        servicio = Servicio.objects.filter(id=servicio_id).first()
        if not servicio:
            return {'error': 'El servicio especificado no existe.', 'status': 404}

        # Convertir la fecha y hora a objetos datetime
        fecha_reserva = datetime.strptime(fecha, '%Y-%m-%d').date()
        hora_reserva = datetime.strptime(hora_str, '%I:%M %p').time()

        # Combinar fecha y hora en un solo datetime
        reserva_datetime = timezone.make_aware(datetime.combine(fecha_reserva, hora_reserva))

        # Verificar que la fecha y hora seleccionada no sean pasadas
        ahora = timezone.now()
        if reserva_datetime < ahora:
            return {'error': 'No puedes reservar una fecha y hora pasadas.', 'status': 400}

        # Verificar que la reserva sea al menos 2 horas más tarde
        if reserva_datetime - ahora < timedelta(hours=2):
            return {'error': 'La hora de la reserva debe ser al menos 2 horas más tarde de la hora actual.', 'status': 400}

        # Verificar si ya existe una reserva para el mismo servicio, fecha y hora
        reserva_existente = Reserva.objects.filter(
            servicio=servicio, fecha=fecha_reserva, hora=hora_str
        ).exists()

        if reserva_existente:
            return {'error': 'La hora seleccionada ya está reservada para este servicio en esta fecha.', 'status': 400}

        nueva_reserva = Reserva(
            servicio=servicio,
            usuario=usuario,
            fecha=fecha_reserva,
            hora=hora_str
        )
        nueva_reserva.save()

        return {'success': 'Reserva creada con éxito.', 'status': 201}

    except Exception as e:
        return {'error': str(e), 'status': 500}

def crear_reserva(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            servicio_id = data.get('servicio_id')
            fecha = data.get('fecha')
            hora_str = data.get('hora')

            username_logueado = request.session['logueo']['username']
            usuario = Usuario.objects.get(username=username_logueado)

            # Llamar a la función auxiliar para crear la reserva
            resultado = crear_reserva_auxiliar(servicio_id, fecha, hora_str, usuario)
            return JsonResponse({'success': resultado['success']}, status=resultado['status']) if 'success' in resultado else JsonResponse({'error': resultado['error']}, status=resultado['status'])

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al procesar los datos JSON.'}, status=400)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def crear_reserva_secre(request):
    if not request.user.is_authenticated or request.user.rol not in ['SECRE', 'ADMIN']:
        return JsonResponse({'error': 'No tienes permiso para crear una reserva.'}, status=403)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            identificacion = data.get('identificacion')
            servicio_id = data.get('servicio_id')
            fecha = data.get('fecha')
            hora_str = data.get('hora')

            # Obtener el usuario asociado
            usuario = Usuario.objects.get(username=identificacion)

            request_data = {
                'servicio_id': servicio_id,
                'fecha': fecha,
                'hora': hora_str
            }
            request._body = json.dumps(request_data)
            request.session['logueo'] = {'username': usuario.username}

            return crear_reserva(request)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Error al procesar los datos JSON.'}, status=400)
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)


#######################################################################################

def listar_reservas(request):
    if 'logueo' not in request.session:
        return JsonResponse({'error': 'Usuario no autenticado.'}, status=401)

    username_logueado = request.session['logueo']['username']
    
    try:
        usuario = Usuario.objects.get(username=username_logueado)

        # Obtener las reservas
        if usuario.rol in ['ESPEC', 'ADMIN']:
            reservas = Reserva.objects.exclude(estado__in=["A", "C", "N"])  # Excluir estados atendido, cancelado y no atendido
            es_especialista = True
        elif usuario.rol == 'SECRE':
            reservas = Reserva.objects.exclude(estado__in=["A", "C", "N"])  
            es_especialista = False  # No es especialista            
        else:
            reservas = Reserva.objects.filter(usuario=usuario).exclude(estado__in=["A", "C", "N"])  
            es_especialista = False

        # Verificar si la fecha y la hora de la reserva han pasado y actualizar el estado
        ahora = datetime.now()
        for reserva in reservas:
            # Asegurarse de que reserva.hora sea un objeto datetime.time
            if isinstance(reserva.hora, str):
                reserva_hora = datetime.strptime(reserva.hora, '%I:%M %p').time()
            else:
                reserva_hora = reserva.hora

            fecha_hora_reserva = datetime.combine(reserva.fecha, reserva_hora)
            if fecha_hora_reserva < ahora and reserva.estado not in ["A", "C", "N"]:
                reserva.estado = "N"  # Cambiar el estado a "no atendido"
                reserva.save()


        if not reservas.exists():
            return JsonResponse({'error': 'No hay reservas disponibles.'}, status=404)

        reservas_data = []
        for reserva in reservas:
            reservas_data.append({
                'id': reserva.id,
                'servicio': {
                    'nombreServicio': reserva.servicio.nombreServicio,
                    'precio': reserva.servicio.precio,
                },
                'usuario': {
                    'username': reserva.usuario.username,  
                    'id': reserva.usuario.id, 
                    'nombre': reserva.usuario.nombre,  
                },
                'fecha': reserva.fecha.isoformat() if reserva.fecha else None,
                'hora': reserva.hora,
                'es_especialista': es_especialista,  #agrega el rol
                'es_secre': usuario.rol == 'SECRE',
                'es_admin': usuario.rol == 'ADMIN',
            })

        return JsonResponse({'reservas': reservas_data})

    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


#--------------------------------------------------------------------
#-------------------------------------------------------------

def confirmar_reserva(request):
    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')

        try:
            reserva = Reserva.objects.get(id=reserva_id)
            reserva.estado = "A"
            reserva.save()
            return JsonResponse({'success': True})
        except Reserva.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Reserva no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def cancelar_reserva(request):
    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')
        username_logueado = request.session.get('logueo', {}).get('username', None)

        try:
            reserva_id = int(reserva_id)  
            reserva = Reserva.objects.get(id=reserva_id)  #
            reserva.estado = "C" 
            reserva.usuario_cancelacion = username_logueado  
            reserva.save()  
            return JsonResponse({'success': True})

        except Reserva.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Reserva no encontrada'})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'ID de reserva inválido'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

#-------------------------------------------------------------

def buscar_usuarioSecre(request):
    username = request.GET.get('username')
    print(f"Identificación recibida: {username}")

    if username:
        try:
            usuario = Usuario.objects.get(username=username)
            if usuario.rol != 'USUAR':
                error_message = "No se puede crear una reserva para este usuario. Comuníquese con el administrador."
                return render(request, 'reservas/crear_reserva_secre.html', {
                    'error_message': error_message,
                    'servicios': Servicio.objects.all()
                })
            return render(request, 'reservas/crear_reserva_secre.html', {
                'usuario': usuario,
                'servicios': Servicio.objects.all()
            })
        except Usuario.DoesNotExist:
            error_message = "El usuario no existe. Primero debe crear una cuenta."
            return render(request, 'reservas/crear_reserva_secre.html', {
                'error_message': error_message,
                'servicios': Servicio.objects.all()
            })
    return render(request, 'reservas/crear_reserva_secre.html', {
        'error_message': 'Parámetro username no proporcionado',
        'servicios': Servicio.objects.all()
    })

#--------------------------------------Renderizacion de paginas----------------------------------------------------#

@role_required(["ADMIN","USUAR"])
def reservas(request):
    return render(request, "reservas/reservas.html")

@role_required(["ADMIN","SECRE"])
def crear_reserva_secre(request):
    return render(request, "reservas/crear_reserva_secre.html")

@role_required(["ADMIN","USUAR","SECRE","ESPEC"])
def misReservas(request):
    return render(request, "reservas/misReservas.html")

@role_required(["ADMIN","SECRE","ESPEC"])
def buscarHistoriaClinica(request):
    return render(request, "historiaClinica/buscarHistoriaClinica.html")


def servicios(request):
    servicios = Servicio.objects.all()  
    # Verifica la URL para determinar qué template cargar
    if 'reservas' in request.path:
        template = "reservas/reservas.html"
    elif 'buscarServicio' in request.path:  
        template = "servicios/buscarServicio.html"
    else:
        template = "servicios/servicios.html"

    return render(request, template, {'servicios': servicios})

@role_required(["ADMIN"])
def busquedaServicio(request):
    if request.method == "POST":
        dato = request.POST.get("servicios_buscar")
        if dato:
            # Filtra los servicios por nombre o especialista (cambia a nombre correcto si es diferente)
            servicios = Servicio.objects.filter(Q(nombreServicio__icontains=dato) | Q(nombreEspecialista__icontains=dato))
            context = {"servicios": servicios}
            return render(request, "servicios/buscarServicio.html", context)
        else:
            messages.warning(request, "No se enviaron datos para buscar.")
            return redirect("buscarServicio")
    else:
        messages.warning(request, "Método no permitido.")
        return redirect("buscarServicio")


#----------------------------------------------------------------------------------------#

def registrarUsuario(request):
    return render(request, "usuarios/registrarUsuario.html")

@role_required(["ADMIN"])
def registrarUsuario2(request):
    return render(request, "usuarios/registrarUsuario2.html")
#-----------------------------------------------------------------------------------------#


@role_required(["ADMIN"])
def buscarUsuario(request):
    q = Usuario.objects.all()

    roles_alias = {
        'ADMIN': 'Administrador',
        'SECRE': 'Secretaria',
        'ESPEC': 'Especialista',
        'USUAR': 'Cliente'
    }

    usuarios_con_alias = []
    for usuario in q:
        usuarios_con_alias.append({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'tipo_documento': usuario.tipo_documento,
            'username': usuario.username,
            'rol_alias': roles_alias.get(usuario.rol, usuario.rol)
        })

    contexto = {"data": usuarios_con_alias}
    return render(request, "usuarios/buscarUsuario.html", contexto)

@role_required(["ADMIN"])
def usuario_editar(request, id_Usuario):
    usuario = get_object_or_404(Usuario, pk=id_Usuario)

    if request.method == 'POST':
        return usuario_actualizar(request)

    # Formatear la fecha de nacimiento solo si existe
    formato = usuario.fecha_nacimiento.strftime('%Y-%m-%d') if usuario.fecha_nacimiento else ''

    datos = {
        "registro": usuario,
        "fecha_nacimiento": formato  
    }
    return render(request, "usuarios/editarUsuario.html", datos)


def usuario_actualizar(request):
    # Busca el usuario por su ID
    c = get_object_or_404(Usuario, pk=request.POST.get("id"))
    
    try:
        c.nombre = request.POST.get("nombre")
        c.apellido = request.POST.get("apellido")
        c.fecha_nacimiento = request.POST.get("fecha_nacimiento")
        c.email = request.POST.get("correo")
        c.username = request.POST.get("identificacion")
        c.tipo_documento = request.POST.get("tipoIdentificacion")
        c.rol = request.POST.get("rol")
        
        # Manejo de la imagen de perfil
        if 'foto' in request.FILES:
            c.foto = request.FILES['foto']
        c.save()
        
        messages.success(request, "Registro actualizado correctamente!!")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    
    return redirect("buscarUsuario")


def eliminar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)

    if usuario.rol == "ADMIN" and usuario.username == "admin_predeterminado":
        messages.error(request, "No se puede eliminar al administrador predeterminado.")
        return redirect("buscarUsuario")
    
    try:
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
    except ValidationError as e:
        messages.error(request, str(e))
    
    return redirect("buscarUsuario")
#----------------------------------------------------------------------------------#

@role_required(["ADMIN","SECRE","ESPEC"])
def buscar_identificacion(request):
    identificacion_url = request.GET.get('identificacion')
    reserva_id = request.GET.get('reserva_id')
    fecha_reserva = request.GET.get('fecha_reserva')

    if not identificacion_url:
        return render(request, 'historiaClinica/buscarHistoriaClinica.html', {
            'historias_clinicas': [],
            'identificacion_consultada': identificacion_url,
            'reserva_id': reserva_id,
            'fecha_reserva': fecha_reserva,
            'mostrar_todas': False,
            'puede_crear_historia': False
        })

    username_logueado = request.session.get('logueo', {}).get('username', None)

    if username_logueado:
        usuario_logueado = Usuario.objects.get(username=username_logueado)
        rol_usuario = usuario_logueado.rol
    else:
        rol_usuario = None

    puede_crear_historia = rol_usuario in ['ADMIN', 'ESPEC']

    try:
        paciente = Usuario.objects.get(username=identificacion_url)
        nombre = paciente.nombre
        apellido = paciente.apellido
        fecha_nacimiento = paciente.fecha_nacimiento
        telefono = paciente.telefono
        print(f"Datos recibidos: Identificación={identificacion_url}, Reserva ID={reserva_id}, Fecha Reserva={fecha_reserva}")

        mostrar_todas = request.GET.get('mostrar_todas', 'false')

    except Usuario.DoesNotExist:
        messages.error(request, 'El paciente no existe. Por favor verifica la identificación.')
        return render(request, 'historiaClinica/buscarHistoriaClinica.html', {
            'historias_clinicas': [],
            'identificacion_consultada': identificacion_url,
            'reserva_id': reserva_id,
            'fecha_reserva': fecha_reserva,
            'rol_usuario': rol_usuario,
            'mostrar_todas': False,
            'puede_crear_historia': puede_crear_historia
        })

    if paciente:
        historias_clinicas = HistoriaClinica.objects.filter(paciente__username=identificacion_url).order_by('-fecha')

        if historias_clinicas.exists():
            historias_a_mostrar = historias_clinicas if mostrar_todas == 'true' else historias_clinicas[:1]
            return render(request, 'historiaClinica/buscarHistoriaClinica.html', {
                'historias_clinicas': historias_a_mostrar,
                'identificacion_consultada': identificacion_url,
                'mostrar_todas': mostrar_todas == 'true',
                'reserva_id': reserva_id,
                'fecha_reserva': fecha_reserva,
                'rol_usuario': rol_usuario,
                'puede_crear_historia': puede_crear_historia
            })
        else:
            return render(request, 'historiaClinica/buscarHistoriaClinica.html', {
                'historias_clinicas': [],
                'identificacion_consultada': identificacion_url,
                'reserva_id': reserva_id,
                'fecha_reserva': fecha_reserva,
                'rol_usuario': rol_usuario,
                'mostrar_todas': False,
                'mostrar_mensaje_creacion': True,
                'puede_crear_historia': puede_crear_historia
            })


def crear_historia_clinica(request, identificacion):
    nombre = ''
    apellido = ''
    fecha_nacimiento = ''
    telefono = ''
    fecha_sesion = timezone.now().date()  

    reserva_id = request.GET.get('reserva_id')
    fecha_reserva = request.GET.get('fecha_reserva')

    try:
        paciente = Usuario.objects.get(username=identificacion)
        nombre = paciente.nombre
        apellido = paciente.apellido
        fecha_nacimiento = paciente.fecha_nacimiento
        telefono = paciente.telefono

    except Usuario.DoesNotExist:
        messages.error(request, 'El paciente no existe. Por favor verifica la identificación.')
        return redirect('buscarIdentificacion')  

    #  última historia clínica si existe
    ultima_historia_clinica = paciente.paciente_historia.last() if paciente.paciente_historia.exists() else None
    observaciones_anteriores = ultima_historia_clinica.observaciones if ultima_historia_clinica else ''

    if request.method == 'POST':
        telefono_nuevo = request.POST.get('telefono')
        observacion_medica = request.POST.get('observacionMedica')  
        motivo_consulta = request.POST.get('motivoConsulta')
        observaciones_nuevas = request.POST.get('observaciones')  
        tratamiento_id = request.POST.get('tratamiento')  #

        # trae el tratamiento seleccionado desde la base de datos
        tratamiento = get_object_or_404(Servicio, id=tratamiento_id)

        # Actualiza el teléfono del paciente si es diferente al actual
        if telefono_nuevo and telefono_nuevo != paciente.telefono:
            paciente.telefono = telefono_nuevo
            paciente.save()

        # Anexar únicamente las "Nuevas Observaciones Médicas" a las observaciones anteriores
        observaciones_medicas_actualizadas = observaciones_anteriores
        if observacion_medica:
            observaciones_medicas_actualizadas = f"{observaciones_anteriores}\n{observacion_medica}" if observaciones_anteriores else observacion_medica

        try:
            user_id = request.session['logueo']['id']
            especialista = Usuario.objects.get(id=user_id)
        except KeyError:
            messages.error(request, 'No se pudo obtener el ID del usuario desde la sesión.')
            return redirect('buscarIdentificacion')
        except Usuario.DoesNotExist:
            messages.error(request, 'El especialista no existe. Por favor verifica la autenticación.')
            return redirect('buscarIdentificacion')

        if especialista.rol != 'ESPEC':
            messages.error(request, 'Solo los especialistas pueden crear historias clínicas.')
            return redirect('buscarIdentificacion')

        # Crear la nueva historia clínica con las "Nuevas Observaciones Médicas" actualizadas
        historia_clinica = HistoriaClinica.objects.create(
            paciente=paciente,
            especialista=especialista,  
            evolucion=observaciones_nuevas,  # Guardar "Observaciones Nuevas" por separado
            diagnostico=motivo_consulta,  # Se usa 'diagnostico' para motivo de consulta
            tratamiento=tratamiento,  # Asignar el tratamiento seleccionado
            observaciones=observaciones_medicas_actualizadas,    # Actualizar solo "Nuevas Observaciones Médicas" con el historial anterior
            fecha=fecha_sesion,  # Se usa la fecha de sesión actual
            reserva_id=reserva_id, 
            fecha_reserva=fecha_reserva  
        )
        
        messages.success(request, 'Historia clínica creada con éxito.')
        return redirect('buscarIdentificacion')


    servicios = Servicio.objects.all()  

    return render(request, 'historiaClinica/crearHistoriaClinica.html', {
        'identificacion': identificacion,
        'nombre': nombre,
        'apellido': apellido,
        'fecha_nacimiento': fecha_nacimiento,
        'telefono': telefono,
        'fecha_sesion': fecha_sesion,  
        'servicios': servicios,  # Pasar los servicios disponibles 
        'observaciones_anteriores': observaciones_anteriores,  
        'reserva_id': reserva_id,  
        'fecha_reserva': fecha_reserva 
    })



##################################################    

def verificar_token_form(request, email):
	if request.method == "POST":
		try:
			q = Usuario.objects.get(email=email)
			if q.token != "" and q.token == request.POST.get("token"):
				messages.success(request, "validacion correcta, cambie su clave!!")
				return redirect("olvide_mi_clave", email=email)
			else:
				messages.error(request, "validacion inccorrecta...")
		except Usuario.DoesNotExist:
			messages.error(request, "El Usuario no existe...")

		return redirect("verificar_token_form", email=email)
	else:
		contexto = { "email": email }
		return render(request, "./login/verificar_token_form.html", contexto)

def olvide_mi_clave(request, email):
    if request.method == "POST":
        c_nueva1 = request.POST.get("nueva1")
        c_nueva2 = request.POST.get("nueva2")

        q = Usuario.objects.get(email=email)

        if c_nueva1 == c_nueva2:
            error = validar_clave(c_nueva1)
            if error:
                messages.warning(request, error)
                return redirect("olvide_mi_clave", email=email)

            password = hash_password(c_nueva1)
            q.password = password
            # Eliminar el token de db
            q.token = ""
            q.save()

            messages.success(request, "Clave cambiada correctamente!!")
            return redirect("index")
        else:
            messages.warning(request, "Claves nuevas no concuerdan...")

        return redirect("olvide_mi_clave", email=email)
    else:
        contexto = {"email": email}
        return render(request, "./login/olvide_mi_clave.html", contexto)

def enviar_correo(ruta, email, token):
	from django.core.mail import BadHeaderError, EmailMessage
	destinatario = email
	mensaje = f"""
			<h1 style='color:blue;'>Massage\nTheraphy</h1>
            <p>Hola!</p>
			<p>Identificamos que usted realizó una solicitud de cambio de clave.</p>
			<p>Haga click aquí:</p>
			<br>
			<a href='http://127.0.0.1:8000/{ruta}'>Recuperar contraseña </a>
			<br>
			<p>Digite el siguiente token: <strong>{token}</strong></p>
			<p>Si no fuiste tu comunicate de inmediato al siguiente correo: <strong>massagetherapyitech@gmail.com</strong></p>
			"""
	print(mensaje)
	try:
		msg = EmailMessage("Soporte Massage therapy", mensaje, settings.EMAIL_HOST_USER, [destinatario])
		msg.content_subtype = "html"  # Habilitar contenido html
		msg.send()
		return "recuperacion enviada, verifique su cuenta de correo electrónico."
	except BadHeaderError:
		return "Encabezado no válido"
	except Exception as e:
		return f"Error: {e}"

def recuperar_clave_form(request):
	if request.method == "POST":
		try:
			q = Usuario.objects.get(email=request.POST.get("correo"))
			num = randint(100000, 999999)
			# convertir num a base64 para ocultarlo un poco
			ofuscado = base64.b64encode(str(num).encode("ascii")).decode("ascii")
			q.token = ofuscado
			q.save()

			# envío de correo
			ruta = reverse(verificar_token_form, args=(q.email,))

			resultado = enviar_correo(ruta, q.email, q.token)
			messages.info(request, resultado)
			return redirect("verificar_token_form", email=q.email)
		except Usuario.DoesNotExist:
			messages.error(request, "Usuario no existe...")

		return redirect("recuperar_clave_form")
	else:
		return render(request, "./login/recuperar_clave_form.html")



def validar_clave(clave):
    if len(clave) < 4:
        return "La clave debe tener al menos 4 caracteres."
    if len(clave) > 10:
        return "La clave no debe tener más de 10 caracteres."    
    if not any(char.isdigit() for char in clave):
        return "La clave debe contener al menos un número."
    # if not any(char.isupper() for char in clave):
    #     return "La clave debe contener al menos una letra mayúscula."
    # if not any(char.islower() for char in clave):
    #     return "La clave debe contener al menos una letra minúscula."
    # if not any(char in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for char in clave):
    #     return "La clave debe contener al menos un carácter especial."
    return None

def cambiar_clave(request):
    logueo = request.session.get("logueo", False)

    if logueo:
        if request.method == "POST":
            actual = request.POST.get("actual")
            nueva1 = request.POST.get("nueva1")
            nueva2 = request.POST.get("nueva2")

            try:
                usuario = Usuario.objects.get(id=logueo["id"])
                if check_password(actual, usuario.password):
                    if nueva1 == nueva2:
                        error = validar_clave(nueva1)
                        if error:
                            messages.error(request, error)
                        else:
                            usuario.password = make_password(nueva1)
                            usuario.save()
                            messages.success(request, "Clave cambiada correctamente.")
                            return redirect("index")
                    else:
                        messages.error(request, "Las nuevas claves no coinciden.")
                else:
                    messages.error(request, "La clave actual es incorrecta.")
            except Usuario.DoesNotExist:
                messages.error(request, "Usuario no encontrado.")
        
        return render(request, "./login/cambiar_clave.html")
    else:
        messages.info(request, "No tiene permisos para acceder al módulo...")
        return redirect("index")

@role_required(["ADMIN"])
def registrarServicio(request):
    return render(request, "servicios/registrarServicio.html")


def eliminarServicio(request, servicio_id):
    if request.method == 'DELETE':
        print('ID del servicio que se va a eliminar:', servicio_id)  
        servicio = get_object_or_404(Servicio, id=servicio_id)

        reservas_url = 'http://127.0.0.1:8000/api/1.0/reserva/'  
        try:
            response = requests.get(reservas_url)
            reservas = response.json()

            print('Reservas obtenidas:', reservas)  

            # Verifica si el ID del servicio está en alguna reserva
            servicio_en_reserva = any(reserva['servicio'] == servicio_id for reserva in reservas)
            for reserva in reservas:
                print('Comparando servicio en reserva:', reserva['servicio'], 'con ID:', servicio_id)  

            if servicio_en_reserva:
                return JsonResponse(
                    {'error': 'Este servicio tiene reservas asociadas y no puede ser eliminado.'},
                    status=400
                )

            # Si no hay reservas asociadas, eliminar el servicio
            servicio.delete()
            return JsonResponse({'message': 'El servicio fue eliminado correctamente.'}, status=200)

        except requests.exceptions.RequestException as e:
            print('Error al verificar reservas:', e)  # Log de error
            return JsonResponse({'error': 'Error al verificar reservas: ' + str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def buscarServicio(request):
    servicios = Servicio.objects.all()
    context = {"servicios": servicios}
    return render(request, "servicios/buscarServicio.html", context)

@role_required(["ADMIN"])
def editarServicio(request,id):
    servicio = get_object_or_404(Servicio, pk=id)
    return render(request, "servicios/editarServicio.html", {'servicio': servicio})


def actualizarServicio(request, id):
    servicio = get_object_or_404(Servicio, pk=id)
    if request.method == 'POST':
        try:
            servicio.nombreServicio = request.POST['nombreServicio']
            servicio.descripcion = request.POST['descripcion']
            servicio.nombreEspecialista = request.POST['nombreEspecialista']
            precio = request.POST['precio']

            # Validación para el precio
            if not precio.isdigit():  # Verificar que el precio es un número
                messages.error(request, 'El precio debe ser un número.')
                return redirect('editarServicio', id=id)
            precio = float(precio)
            if precio < 100:
                messages.error(request, 'El precio no puede ser menor a 100.')
                return redirect('editarServicio', id=id)
            if precio > 999_000_000:
                messages.error(request, 'El precio no puede ser mayor a 999 millones.')
                return redirect('editarServicio', id=id)

            servicio.precio = precio
            servicio.save()
            messages.success(request, 'Servicio actualizado correctamente.')
            return redirect('buscarServicio')
        except Exception as e:
            messages.error(request, f'Error al actualizar el servicio: {str(e)}')
            return redirect('editarServicio', id=id)
    return render(request, 'editarServicio.html', {'servicio': servicio})


def obtener_especialistas(request):
    if request.method == 'GET':
        especialistas = User.objects.filter(groups__name='ESPEC')
        # formatea la respuesta con el ID y nombre 
        data = [{"id": e.id, "nombre": f"{e.first_name} {e.last_name}"} for e in especialistas]
        return JsonResponse(data, safe=False)
    return JsonResponse({"error": "Método no permitido"}, status=405)

#_________________________________vista de prueba calendario____________________________________

def calendario(request):
    all_events = Events.objects.all()
    context = {
        "events": all_events,
    }
    return render(request, "citas/calendario.html", context)

def all_events(request):
    all_events = Events.objects.all()
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
        })

    return JsonResponse(out, safe=False)


def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)

def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)



def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)
# _________________________Vista para la API_________________________

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer


class HistoriaClinicaViewSet(viewsets.ModelViewSet):
    queryset = HistoriaClinica.objects.all()
    serializer_class = HistoriaClinicaSerializer


class CitaServicioViewSet(viewsets.ModelViewSet):
    queryset = CitaServicio.objects.all()
    serializer_class = CitaServicioSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
