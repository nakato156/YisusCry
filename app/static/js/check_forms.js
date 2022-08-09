function not_empty(formulario, excludes){
    for( [name, val] of formulario){
        formulario[name] = val.trim()
        if(excludes && excludes.includes(name)) continue;
        else if(!val.trim()) {
            Swal.fire({
                icon: 'info',
                title: 'Debe llenar todos los campos'
            })
            return false;
        }
    }
    return true;
}