

function verDetalles(servicioId) {
    window.location.href = `/detallesServicio/${servicioId}`;
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

    // Cargar especialistas al inicio
    const especialistaActual = "{{ servicio.nombreEspecialista }}";
    cargarEspecialistas(especialistaActual);

    // Guardar cambios con validaciones
    document.getElementById('guardarBtn').addEventListener('click', function () {
        const servicioId = this.getAttribute('data-servicio-id');
        const nombreServicio = document.getElementById('nombreServicio').value.trim();
        const descripcion = document.getElementById('descripcion').value.trim();
        const nombreEspecialista = document.getElementById('nombreEspecialista').value.trim();
        const precio = document.getElementById('precio').value.trim();

        // Validaciones
        if (!nombreServicio) {
            alert("El nombre del servicio es obligatorio.");
            return;
        }

        if (!descripcion) {
            alert("La descripción es obligatoria.");
            return;
        }

        if (!nombreEspecialista) {
            alert("Debe seleccionar un especialista.");
            return;
        }

        if (!precio) {
            alert("El precio es obligatorio.");
            return;
        }

        if (isNaN(precio)) {
            alert("El precio debe ser un número válido.");
            return;
        }

        const precioNumerico = parseFloat(precio);

        if (precioNumerico < 100) {
            alert("El precio no puede ser menor a 100.");
            return;
        }

        if (precioNumerico > 999_000_000) {
            alert("El precio no puede ser mayor a 999,000,000.");
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
            precio: precioNumerico
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
