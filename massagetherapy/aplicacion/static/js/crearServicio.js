
document.addEventListener('DOMContentLoaded', function () {
    const cargarEspecialistas = () => {
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
                    option.value = `${especialista.nombre} ${especialista.apellido}`; // Enviar el nombre completo
                    option.textContent = `${especialista.nombre} ${especialista.apellido}`; // Mostrar nombre y apellido
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

    cargarEspecialistas();


    //////////////////////////registrar servicio////////////////////////


    document.getElementById('registrarServicioForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const nombreServicio = document.getElementById('nombreServicio').value;
        const descripcion = document.getElementById('descripcion').value;
        const nombreEspecialista = document.getElementById('nombreEspecialista').value; // Nombre completo
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
            nombreEspecialista: nombreEspecialista, // Nombre completo enviado al backend
            precio: parseFloat(precio)
        };

        fetch('http://127.0.0.1:8000/api/1.0/servicio/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        })
            .then(response => {
                if (response.ok) {
                    document.getElementById('mensajeExito').style.display = 'block';
                    document.getElementById('registrarServicioForm').reset();
                    setTimeout(() => {
                        window.location.href = '/buscarServicio/';
                    }, 1000);
                } else {
                    document.getElementById('mensajeError').style.display = 'block';
                }
            })
            .catch(error => {
                console.error('Error al enviar los datos:', error);
                document.getElementById('mensajeError').style.display = 'block';
            });
    });
});
