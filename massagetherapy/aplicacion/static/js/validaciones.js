document.addEventListener('DOMContentLoaded', () => {
    const formRegistrar = document.getElementById('formRegistrar');
    const tipoIdentificacion = formRegistrar.elements['tipoIdentificacion'];
    const clave1 = document.getElementById('clave1');
    const clave2 = document.getElementById('clave2');
    const correo = formRegistrar.elements['correo'];
    const identificacion = formRegistrar.elements['identificacion'];
    const btnReg = document.getElementById('btnReg');

    btnReg.addEventListener('click', (event) => {
        let valid = true;
        let mensajeError = "";

        // Validación del tipo de identificación
        if (tipoIdentificacion.value === "" || tipoIdentificacion.value === "- Selecciona -") {
            mensajeError += "Por favor, selecciona un tipo de identificación válido.\n";
            valid = false;
        }

        // Validación de contraseñas
        if (clave1.value !== clave2.value) {
            mensajeError += "Las contraseñas no coinciden.\n";
            valid = false;
        }

        // Validación del correo electrónico
        const correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!correoRegex.test(correo.value)) {
            mensajeError += "Por favor, ingresa un correo electrónico válido.\n";
            valid = false;
        }

        // Validación de identificación
        const identificacionRegex = /^[0-9]{5,10}$/;
        if (!identificacionRegex.test(identificacion.value)) {
            mensajeError += "El número de identificación debe contener entre 5 y 10 dígitos.\n";
            valid = false;
        }

        // Mostrar errores si los hay
        if (!valid) {
            alert(mensajeError); // Muestra los errores en un mensaje de alerta
            event.preventDefault(); // Detiene el envío del formulario
        }
    });
});
