function analizarCodigo() {
    const form = document.getElementById('analizador-form');
    const formData = new FormData(form);

    console.log(...formData);  // Esto te mostrará los datos que se están enviando

    fetch('/analizar', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        console.log(data); // Mostrar el resultado en la consola
        document.getElementById('resultado').value = data;  // Mostrar el resultado en el textarea
    })
    .catch(error => {
        console.error('Error al enviar el formulario:', error);
    });
}
/*
function borrarCampos() {
    document.querySelector('textarea[name=codigo_fuente]').value = '';
    document.getElementById('resultado').value = '';
    document.getElementById("file-input").value ='';
}
*/
function borrarCampos() {
    const input = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name');
    const textArea = document.querySelector('textarea[name="codigo_fuente"]');
    const resultado = document.getElementById('resultado');

    // Limpiar el input de archivo
    input.value = "";
    // Actualizar el texto a "Seleccionar archivos"
    fileNameDisplay.textContent = "Seleccionar archivos";
    // Limpiar el área de texto
    textArea.value = "";
    // Limpiar el área de resultado
    resultado.value = "";
}
