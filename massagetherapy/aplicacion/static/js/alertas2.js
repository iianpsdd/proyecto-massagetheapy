$(document).ready(function () {
    // Obtener el token CSRF (manteniendo la lógica que ya tienes)
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
        beforeSend: function(xhr, settings) {
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
            $.ajax({
                url: url,
                type: 'POST',
                data: formData,
                success: function (response) {
                    if (response.success) {
                        window.location.href = response.next; // Redirige a la URL proporcionada en 'next'
                    } else {
                        alert(response.message);
                    }
                },
                error: function (xhr, errmsg, err) {
                    alert("Error: " + errmsg);
                }
            });
        } else if (idElemento === 'formRegistrar') {
            // Manejo para el registro
            datosAjax(url, formData, 'registrarUsuario');
        }
    });

    // Asignar la URL de redirección cuando el modal se abra
    $('#loginModal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget); // Botón que activó el modal
        var nextUrl = button.data('next'); // Extrae la URL de redirección
        $(this).find('#next').val(nextUrl); // Establece el valor del campo 'next'
    });

    // Función para manejar la solicitud AJAX
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
});
