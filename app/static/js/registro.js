window.onload = init

function init(){
    const form = document.getElementById("formulario")
    form.addEventListener("submit", async e => {
        e.preventDefault()
        const data = new FormData(form)
        const req = await fetch("/registro", {
            method: "POST",
            body: data
        })
        const res = await req.json()
        const info = await res

        if (res.status){
           Swal.fire({
              position: 'center',
              icon: 'success',
              title: 'Registrado satisfactoriamente',
              showConfirmButton: false,
              timer: 1500
           })
           setTimeout(1501, ()=>window.location.href="../perfil")
        }else {
            Swal.fire({
              icon: 'error',
              title: info.error,
              text: info.server ? 'Error del servidor' : 'Verifique que el nombre de usuario, correo o código no hayan sido registrados',
            })
        }
    })
 }
