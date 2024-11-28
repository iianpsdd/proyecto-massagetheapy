// Obtener el token CSRF del cookie
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

const csrftoken = getCookie('csrftoken');

// Función para crear una reserva
function crearReserva(servicioId, fecha, hora) {
    const identificacion = $('#identificacionHidden').val();
    if (!identificacion) {
        alert('Por favor, selecciona un usuario.');
        return;
    }

    const data = {
        servicio_id: servicioId,
        fecha: fecha,
        hora: hora, // Asegúrate de que la hora tenga el formato adecuado
        identificacion: identificacion // Añadir identificacion del usuario
    };

    $.ajax({
        url: '/creareserva/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (response) {
            console.log('Reserva exitosa:', response);
            alert('Reserva creada con éxito.');
        },
        error: function (error) {
            console.log('Error en la reserva:', error);
            alert('Error en la reserva: ' + error.responseText);
        }
    });
}

// Manejar el envío del formulario de reserva
$(document).ready(function () {
    $('#crearReservaForm').on('submit', function (event) {
        event.preventDefault();
        const servicioId = $('#servicio').val();
        const fecha = $('#fecha').val();
        const hora = $('#hora2').val();
        if (!fecha || !hora) {
            alert('Por favor, selecciona una fecha y hora.');
            return;
        }
        crearReserva(servicioId, fecha, hora);
    });
});