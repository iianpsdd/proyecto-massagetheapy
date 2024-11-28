/* function editarServicio() {
    window.location.href = `/servicios/editarServicio/`;
} */

function verDetalles(servicioId) {
    window.location.href = `/detallesServicio/${servicioId}`;
}


// function eliminarServicio(servicioId) {
//     console.log('ID del servicio que se desea eliminar:', servicioId); // Log del ID del servicio

//     if (confirm('¿Estás seguro de que deseas eliminar este servicio?')) {
//         // Hacer una solicitud para obtener todas las reservas
//         fetch('http://127.0.0.1:8000/api/1.0/reserva/')
//             .then(response => response.json())
//             .then(reservas => {
//                 console.log('Reservas obtenidas:', reservas); // Log del objeto reservas

//                 // Convertir servicioId a número por seguridad
//                 const idServicioNumerico = Number(servicioId);

//                 // Verificar si el servicio está asociado a alguna reserva
//                 const servicioEnReserva = reservas.some(reserva => {
//                     console.log(
//                         'Comparando servicio en reservas:',
//                         reserva.servicio,
//                         'con el ID:',
//                         idServicioNumerico
//                     ); // Log detallado
//                     return Number(reserva.servicio) === idServicioNumerico; // Comparación segura
//                 });

//                 if (servicioEnReserva) {
//                     alert('Este servicio tiene reservas asociadas y no puede ser eliminado.');
//                     return; // Detener ejecución si hay una asociación
//                 }

//                 // Confirmar eliminación del servicio
//                 if (confirm('Este servicio no tiene reservas asociadas, ¿deseas eliminarlo?')) {
//                     fetch(`http://127.0.0.1:8000/api/1.0/servicio/${servicioId}/`, {
//                         method: 'DELETE',
//                         headers: {
//                             'X-CSRFToken': getCookie('csrftoken') // Asegúrate de manejar el token CSRF
//                         }
//                     })
//                         .then(response => {
//                             if (response.ok) {
//                                 alert('Servicio eliminado correctamente.');
//                                 // Eliminar el servicio de la interfaz
//                                 const servicioElemento = document.getElementById(`servicio-${servicioId}`);
//                                 if (servicioElemento) {
//                                     servicioElemento.remove();
//                                 } else {
//                                     console.warn(`No se encontró el elemento con ID: servicio-${servicioId}`);
//                                 }
//                             } else {
//                                 return response.json().then(data => {
//                                     console.log('Error al eliminar servicio:', data); // Log del error
//                                     alert(data.error || 'Hubo un error al intentar eliminar el servicio.');
//                                 });
//                             }
//                         })
//                         .catch(error => {
//                             console.error('Error al eliminar el servicio:', error);
//                             alert('Hubo un error al intentar eliminar el servicio.');
//                         });
//                 } else {
//                     alert('La eliminación ha sido cancelada.');
//                 }
//             })
//             .catch(error => {
//                 console.error('Error al obtener las reservas:', error);
//                 alert('Hubo un error al intentar obtener las reservas.');
//             });
//     } else {
//         alert('La eliminación ha sido cancelada.');
//     }
// }



// Modificación en la lógica del frontend donde se elimina el servicio:
// function eliminarServicio(servicioId) {
//     console.log('ID del servicio que se desea eliminar:', servicioId); // Log del ID del servicio

//     confirmarEliminar('¿Estás seguro de que deseas eliminar este servicio?', (confirmado) => {
//         if (!confirmado) {
//             mostrarMensaje('La eliminación ha sido cancelada.', 'success');
//             return;
//         }

//         // Hacer una solicitud para obtener todas las reservas
//         fetch('http://127.0.0.1:8000/api/1.0/reserva/')
//             .then(response => response.json())
//             .then(reservas => {
//                 console.log('Reservas obtenidas:', reservas); // Log del objeto reservas

//                 const idServicioNumerico = Number(servicioId); // Convertir servicioId a número por seguridad

//                 // Verificar si el servicio está asociado a alguna reserva
//                 const servicioEnReserva = reservas.some(reserva => {
//                     console.log(
//                         'Comparando servicio en reservas:',
//                         reserva.servicio,
//                         'con el ID:',
//                         idServicioNumerico
//                     );
//                     return Number(reserva.servicio) === idServicioNumerico;
//                 });

//                 if (servicioEnReserva) {
//                     mostrarMensaje('Este servicio tiene reservas asociadas y no puede ser eliminado.', 'error');
//                     return;
//                 }

//                 // Confirmar eliminación del servicio
//                 confirmarEliminar('Este servicio no tiene reservas asociadas, ¿deseas eliminarlo?', (confirmado) => {
//                     if (!confirmado) {
//                         mostrarMensaje('La eliminación ha sido cancelada.', 'success');
//                         return;
//                     }

//                     fetch(`http://127.0.0.1:8000/api/1.0/servicio/${servicioId}/`, {
//                         method: 'DELETE',
//                         headers: {
//                             'X-CSRFToken': getCookie('csrftoken') // Asegúrate de manejar el token CSRF
//                         }
//                     })
//                         .then(response => {
//                             if (response.ok) {
//                                 mostrarMensaje('Servicio eliminado correctamente.', 'success');
//                                 // Eliminar el servicio de la interfaz
//                                 const servicioElemento = document.getElementById(`servicio-${servicioId}`);
//                                 if (servicioElemento) {
//                                     servicioElemento.remove();
//                                 } else {
//                                     console.warn('No se encontró el elemento con ID: servicio-${servicioId}');
//                                 }
//                             } else {
//                                 return response.json().then(data => {
//                                     console.log('Error al eliminar servicio:', data); // Log del error
//                                     mostrarMensaje(data.error || 'Hubo un error al intentar eliminar el servicio.', 'error');
//                                 });
//                             }
//                         })
//                         .catch(error => {
//                             console.error('Error al eliminar el servicio:', error);
//                             mostrarMensaje('Hubo un error al intentar eliminar el servicio.', 'error');
//                         });
//                 });
//             })
//             .catch(error => {
//                 console.error('Error al obtener las reservas:', error);
//                 mostrarMensaje('Hubo un error al intentar obtener las reservas.', 'error');
//             });
//     });
// }






// Modificación en la lógica del frontend donde se elimina el servicio:
function eliminarServicio(servicioId) {
    console.log('ID del servicio que se desea eliminar:', servicioId); // Log del ID del servicio

    confirmarEliminar('¿Estás seguro de que deseas eliminar este servicio?', (confirmado) => {
        if (!confirmado) {
            mostrarMensaje('La eliminación ha sido cancelada.', 'success');
            return;
        }

        // Hacer una solicitud para obtener todas las reservas
        fetch('http://127.0.0.1:8000/api/1.0/reserva/')
            .then(response => response.json())
            .then(reservas => {
                console.log('Reservas obtenidas:', reservas); // Log del objeto reservas

                const idServicioNumerico = Number(servicioId); // Convertir servicioId a número por seguridad

                // Verificar si el servicio está asociado a alguna reserva
                const servicioEnReserva = reservas.some(reserva => {
                    console.log(
                        'Comparando servicio en reservas:',
                        reserva.servicio,
                        'con el ID:',
                        idServicioNumerico
                    );
                    return Number(reserva.servicio) === idServicioNumerico;
                });

                if (servicioEnReserva) {
                    mostrarMensaje('Este servicio tiene reservas asociadas y no puede ser eliminado.', 'error');
                    return;
                }

                // Confirmar eliminación del servicio
                confirmarEliminar('Este servicio no tiene reservas asociadas, ¿deseas eliminarlo?', (confirmado) => {
                    if (!confirmado) {
                        mostrarMensaje('La eliminación ha sido cancelada.', 'success');
                        return;
                    }

                    fetch(`http://127.0.0.1:8000/api/1.0/servicio/${servicioId}/`, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken') // Asegúrate de manejar el token CSRF
                        }
                    })
                        .then(response => {
                            if (response.ok) {
                                mostrarMensaje('Servicio eliminado correctamente.', 'success');
                                // Eliminar el servicio de la interfaz
                                const servicioElemento = document.getElementById(`servicio-${servicioId}`);
                                if (servicioElemento) {
                                    servicioElemento.remove();
                                } else {
                                    console.warn('No se encontró el elemento con ID: servicio-${servicioId}');
                                }
                            } else {
                                return response.json().then(data => {
                                    console.log('Error al eliminar servicio:', data); // Log del error
                                    mostrarMensaje(data.error || 'Hubo un error al intentar eliminar el servicio.', 'error');
                                });
                            }
                        })
                        .catch(error => {
                            console.error('Error al eliminar el servicio:', error);
                            mostrarMensaje('Hubo un error al intentar eliminar el servicio.', 'error');
                        });
                });
            })
            .catch(error => {
                console.error('Error al obtener las reservas:', error);
                mostrarMensaje('Hubo un error al intentar obtener las reservas.', 'error');
            });
    });
}




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

//----------------------editar servicio------------
document.addEventListener('DOMContentLoaded', function () {
    const cargarEspecialistas = (especialistaActual) => {
        fetch('http://127.0.0.1:8000/api/1.0/usuario/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al obtener usuarios');
                }
                return response.json();
            })
            .then(data => {
                const selectEspecialista = document.getElementById('nombreEspecialista');
                const especialistas = data.filter(usuario => usuario.rol === 'ESPEC');

                especialistas.forEach(especialista => {
                    const option = document.createElement('option');
                    option.value = `${especialista.nombre} ${especialista.apellido}`; // Nombre completo
                    option.textContent = `${especialista.nombre} ${especialista.apellido}`;
                    if (`${especialista.nombre} ${especialista.apellido}` === especialistaActual) {
                        option.selected = true; // Seleccionar al especialista actual
                    }
                    selectEspecialista.appendChild(option);
                });

                if (especialistas.length === 0) {
                    const option = document.createElement('option');
                    option.textContent = 'No hay especialistas disponibles';
                    option.disabled = true;
                    selectEspecialista.appendChild(option);
                }
            })
            .catch(error => {
                console.error('Error al cargar especialistas:', error);
                alert('No se pudieron cargar los especialistas. Intente nuevamente.');
            });
    };



    // Guardar cambios
    document.getElementById('guardarBtn').addEventListener('click', function () {
        const servicioId = this.getAttribute('data-servicio-id');
        const nombreServicio = document.getElementById('nombreServicio').value;
        const descripcion = document.getElementById('descripcion').value;
        const nombreEspecialista = document.getElementById('nombreEspecialista').value;
        const precio = document.getElementById('precio').value;

        if (!nombreServicio || !descripcion || !nombreEspecialista || !precio) {
            alert("Por favor, completa todos los campos.");
            return;
        }

        const getCookie = (name) => {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === `${name}=`) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        };

        const csrfToken = getCookie('csrftoken');

        const data = {
            nombreServicio: nombreServicio,
            descripcion: descripcion,
            nombreEspecialista: nombreEspecialista,
            precio: parseFloat(precio)
        };

        fetch(`/api/1.0/servicio/${servicioId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.ok) {
                    document.getElementById('mensajeExito').style.display = 'block';
                    document.getElementById('mensajeError').style.display = 'none';
                    setTimeout(() => {
                        window.location.href = '/buscarServicio/';
                    }, 1000);
                } else {
                    throw new Error('Error en la actualización del servicio');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                document.getElementById('mensajeError').style.display = 'block';
                document.getElementById('mensajeExito').style.display = 'none';
            });
    });
});
