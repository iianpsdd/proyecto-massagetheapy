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

    // Manejar el click del botón reservar y abrir el modal
    $('.reservar').on('click', function () {
        var servicioId = $(this).data('servicio-id');
        $('#fechaHoraModal').modal('show');

        $('#formReserva').on('submit', function (event) {
            event.preventDefault();
            const fecha = $('#fecha').val();
            const hora = $('#hora2').val();
            if (!fecha || !hora) {
                alert('Por favor, selecciona una fecha y hora.');
                return;
            }
            crearReserva(servicioId, fecha, hora);
        });
    });

    // Configurar el token CSRF en las peticiones AJAX
    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Función para crear una reserva
    function crearReserva(servicioId, fecha, hora) {
        const data = {
            servicio_id: servicioId,
            fecha: fecha,
            hora: hora // Asegúrate de que la hora tenga el formato adecuado
        };
        $.ajax({
            url: '/creareserva/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (result) {
                alert(result.message || 'Reserva creada con éxito.');
                $('#fechaHoraModal').modal('hide'); // Ocultar el modal
                listarReservas(); // Actualizar la lista de reservas
                window.location.href = '/misReservas/'; // Cambia esto si tu URL es diferente
            },
            error: function (xhr, status, error) {
                const errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : 'Hubo un problema al crear la reserva. Inténtalo de nuevo.';
                console.error('Error:', error);
                alert(errorMessage);
            }
        });
    }
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
                $('#reservasContainer').empty().append('<p> ' + xhr.responseJSON.error + '</p>');
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

///////////////////////////////////////

