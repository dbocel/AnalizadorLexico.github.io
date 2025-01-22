


function showFileName(){
    const input = document.getElementById('file-input');
    const fileNameDisplay = document.getElementById('file-name');

    if(input.files.length > 0){
        //obtener el nombre del archivo seleccionado
        fileNameDisplay.textContent = input.files[0].name;
    }else{
        //Si no se selecciona ninguna archivo, muestra seleccionar archivos o texto por defecto 
        fileNameDisplay.textContent = "Seleccionar archivos";
    }
}

