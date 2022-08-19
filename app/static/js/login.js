window.onload = init

function init(){
    const form = document.getElementById("formulario")
    form.addEventListener("submit", async e => {
        e.preventDefault()
        const data = new FormData(form)
        if(!not_empty(data, ["csrf_token"])) return;
        const req = await fetch("/login", {
            method: "POST",
            headers: {
                'X-CSRFToken': data.get("csrf_token")
            },
            body: data
        })
        const res = req.status == 200 ? await req.json() : req.text();
        const info = await res

        if(info.status) setTimeout(()=>window.location.href = "../perfil", 1200)
        else {
            console.log(info)
            Swal.fire({
              icon: 'error',
              title: 'Datos incorrectos',
              text: 'Verifique los datos ingresados'
            })
        }
    })
}