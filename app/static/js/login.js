window.onload = init

function init(){
    const form = document.getElementById("formulario")
    form.addEventListener("submit", async e => {
        e.preventDefault()
        const data = new FormData(form)
        if(!not_empty(data, ["csrf_token"])) return;
        const req = await fetch("/login", {
            method: "POST",
            body: data
        })
        const res = await req.json()
        const info = await res

        if(info.status) window.location.href = "../perfil"
        else {
            Swal.fire({
              icon: 'error',
              title: 'Datos incorrectos',
              text: 'Verifique los datos ingresados'
            })
        }
    })
}