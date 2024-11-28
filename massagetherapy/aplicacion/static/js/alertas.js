$(document).ready(function () {
    // Obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Configurar el token CSRF en las peticiones AJAX
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Manejar la sumisión de formularios AJAX
    $('.formModal').submit(function (event) {
        event.preventDefault();  // Evita el envío tradicional del formulario

        var formData = $(this).serialize();  // Serializa los datos del formulario
        var idElemento = $(this).attr('id');
        var url = $(this).attr('action');  // Obtén la URL desde el atributo "action"

        // Validar cuál es el formulario que se está enviando
        if (idElemento === 'formLogin') {
            datosAjax(url, formData, 'inicio');
        } else if (idElemento === 'formRegistrar') {
            datosAjax(url, formData, 'registrarUsuario');
        }
    });

    // Función para manejar la solicitud AJAX (Login/Registro)
    function datosAjax(url, formData, redireccion) {
        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            success: function (response) {
                if (response.success) {
                    // Si el registro o inicio de sesión es exitoso, redirige a la página correspondiente
                    window.location.href = '/' + redireccion;
                } else {
                    // Muestra un mensaje de error
                    alert(response.message);
                }
            },
            error: function (xhr, errmsg, err) {
                if (xhr.status === 400 && xhr.responseJSON && xhr.responseJSON.error) {
                    // Mensaje de error específico (como correo ya en uso)
                    alert(xhr.responseJSON.error);
                } else {
                    alert("Error: " + errmsg);
                }
            }
        });
    }

    // funcion para lsitar las reservas

    function listarReservas() {
        $.ajax({
            url: '/listar_reservas/',
            type: 'GET',
            success: function (response) {
                var reservas = response.reservas || [];
                var reservasContainer = $('#reservasContainer');
                reservasContainer.empty();
    
                if (reservas.length > 0) {
                    reservas.forEach(function (reserva) {
                        var cardHtml =
                            '<div class="card mb-4" ' + (reserva.estado === 'C' || reserva.estado === 'N' || reserva.estado === 'A'? 'hidden' : '') + '>' +
                            '<div class="card-body">' +
                            '<h5 class="card-title">' + reserva.servicio.nombreServicio + '</h5>' +
                            '<p class="card-text"><strong>Precio:</strong> $' + reserva.servicio.precio + '</p>' +
                            '<p class="card-text"><strong>identificacion:</strong> ' + reserva.usuario.username + '</p>' +
                            '<p class="card-text"><strong>Nombre:</strong><br> ' + reserva.usuario.nombre + '</p>' +
                            '<p class="card-text"><strong>Fecha de Reserva:</strong> ' + new Date(reserva.fecha + 'T00:00:00').toLocaleDateString('es-ES') + '</p>' +
                            '<p class="card-text"><strong>Hora de Reserva:</strong> ' + reserva.hora + '</p>' +
                            '<a class="btn btn-danger" onclick="confirmarCancelacion(' + reserva.id + ', \'' + reserva.fecha + ' ' + reserva.hora + '\')">Cancelar</a><br><br>';
    
                        // Agregar el botón "Confirmar Cita" si el usuario es especialista
                        if (reserva.es_especialista) {
                            cardHtml +=
                                '<a class="btn btn-success " onclick="confirmarCita(' + reserva.id + ', \'' + reserva.usuario.username + '\', \'' + reserva.fecha + '\')">Confirmar Cita</a>';
                        }
                        // Si es SECRE, no mostrar el botón "Confirmar Cita"
                        if (reserva.es_secre) {
                            // No hacer nada, no se añade el botón
                        }
    
                        cardHtml += '</div></div>';
                        reservasContainer.append(cardHtml);
                    });
                } else {
                    reservasContainer.append('<p>No tienes reservas aún.</p>');
                }
            },
            error: function (xhr) {
                console.error('Error al listar reservas:', xhr.responseJSON.error);
                $('#reservasContainer').empty().append('<p style="text-align: center;"><strong>' + xhr.responseJSON.error + '</strong></p>');

            }
        });
    }

    // Función para confirmar cancelación de reserva

    window.confirmarCancelacion = function (reservaId, fechaHora) {
        var reservaDateTime = new Date(fechaHora);
        var ahora = new Date();

        // Verificar si quedan más de 2 horas
        if ((reservaDateTime - ahora) < (2 * 60 * 60 * 1000)) { // 2 horas en milisegundos
            alert('No puedes cancelar esta reserva porque está a menos de 2 horas.');
            return;
        }

        var confirmar = confirm("¿Estás seguro de que deseas cancelar esta reserva?");
        if (confirmar) {
            $.ajax({
                url: '/cancelar_reserva/',
                type: 'POST',
                data: {
                    'reserva_id': reservaId,
                    'csrfmiddlewaretoken': csrftoken // Asegúrate de que csrftoken esté definido
                },
                success: function (response) {
                    alert('Reserva cancelada con éxito.');
                    listarReservas();
                },
                error: function (xhr) {
                    alert('Error al cancelar la reserva: ' + xhr.responseText);
                }
            });
        }
    };

    // Llamar a listar reservas al cargar la página
    $(document).ready(function () {
        listarReservas();



    });

});



// Función para mostrar el mensaje
function mostrarMensaje(message, tipo, opciones = {}) {
    const mensajeDiv = document.createElement('div');
    mensajeDiv.textContent = message;
    mensajeDiv.style.padding = '10px';
    mensajeDiv.style.margin = '10px 0';
    mensajeDiv.style.borderRadius = '5px';
    mensajeDiv.style.color = 'white';

    // Estilo según el tipo de mensaje
    if (tipo === 'error') {
        mensajeDiv.style.backgroundColor = 'red';
    } else if (tipo === 'success') {
        mensajeDiv.style.backgroundColor = 'green';
    }

    // Crear el overlay
    const overlay = document.createElement('div');
    overlay.classList.add('alert-overlay2');

    // Contenedor de la alerta
    const alertContainer = document.createElement('div');
    alertContainer.classList.add('alert-container2');

    // Mensaje dentro del contenedor
    const alert = document.createElement('div');
    alert.classList.add('alert2');
    alert.appendChild(mensajeDiv);
    alertContainer.appendChild(alert);
    document.body.appendChild(overlay);
    document.body.appendChild(alertContainer);

    // Función de cierre de la alerta
    setTimeout(() => {
        alertContainer.remove();
        overlay.remove();
    }, 2500); // El mensaje desaparecerá después de 2.5 segundos

    // Asegurar que el mensaje se quede visible hasta que el usuario haga algo
    if (opciones.confirm) {
        // Crear los botones de confirmación
        const buttonsContainer = document.createElement('div');
        const aceptarBtn = document.createElement('button');
        const cancelarBtn = document.createElement('button');

        aceptarBtn.textContent = 'Aceptar';
        cancelarBtn.textContent = 'Cancelar';

        // Agregar clases personalizadas
        aceptarBtn.classList.add('aceptar');
        cancelarBtn.classList.add('cancelar');

        aceptarBtn.onclick = () => {
            alertContainer.remove();
            overlay.remove();
            opciones.confirm(true); // Acción confirmada
        };

        cancelarBtn.onclick = () => {
            alertContainer.remove();
            overlay.remove();
            // opciones.confirm(false); // Acción cancelada
        };

        buttonsContainer.appendChild(aceptarBtn);
        buttonsContainer.appendChild(cancelarBtn);
        alert.appendChild(buttonsContainer);
    }
}

// Función personalizada para confirmar
function confirmarEliminar(message, confirmCallback) {
    mostrarMensaje(message, 'error', {
        confirm: confirmCallback
    });
}
