let TOKEN_ = null
let formDataUser = null
let listaRoles = null
let btnActualizar, btnEliminar = null

function init_admin(){
    const form_admin = document.getElementById("form_admin")
    TOKEN_ = document.getElementById("token").value
    btnActualizar = document.getElementById("updateUser")
    btnEliminar = document.getElementById("deleteUser")
    
    const masRoles = document.getElementById("masRoles")
    listaRoles = document.getElementById("listRoles")
    formDataUser = document.getElementById("form_update_user")
    
    masRoles.addEventListener("click", (e)=>addRole(e, listaRoles))

    form_admin.addEventListener("submit", async (e)=>{
        e.preventDefault();
        
        const data = new FormData(form_admin)

        const req = await fetch(`/admin/info-user`, {
            method: "POST",
            headers: {
                'X-CSRFToken': TOKEN_
            },
            body: data
        })
        const res = await req.status == 200 ? await req.json() : await req.text()
        const info = await res
        
        if(info.status){
            const info_user = info.info

            Object.values(formDataUser.elements).forEach(element=>{
                let name = element.name
                if(info_user && info_user[name]) element.value = info_user[name]
                else element.value = "---"
            })

            let lista, mas_roles = ""

            if(info_user.role){
                btnActualizar.disabled = false
                btnEliminar.disabled = false

                lista = crearTemplateLista(Object.values(info_user.role), true)
                mas_roles = crearTemplateLista(Object.values(info_user.masRoles))

            }else {
                btnActualizar.disabled = true
                btnEliminar.disabled = true
            }
            listaRoles.innerHTML = lista
            masRoles.innerHTML = mas_roles
        }
    })

    formDataUser.addEventListener("submit", updateUser)
}

function addRole(e, temp_lista){
    const element = e.target
    if(element.type !== "checkbox") return;
    if(element.checked) temp_lista.appendChild(element.parentNode)
}

function crearTemplateLista(roles, checked=false){
    let lista = ""
    roles.forEach(rol=>{
        lista+=`<li class="list-group-item">
        <input class="form-check-input me-1" type="checkbox" value="${rol}" ${checked ? 'checked': ''}>
        <label class="form-check-label">${rol}</label>
      </li>`
    })
    return lista;
}

async function updateUser(e){
    e.preventDefault()
    
    const data = new FormData(formDataUser)
    
    let roles = Object.values(listaRoles.children)
    if(roles.length == 0) return alert("No hay roles. Vuelva a consultar el usuario")

    roles = roles.map(rol=> rol.children[0].checked ? rol.children[0].value : "").join(",")
    data.append("roles", roles)

    const req = await fetch('/admin/user-update', {
        method: "PUT",
        headers: {
            'X-CSRFToken': TOKEN_
        },
        body: data
    })
    const res = await req.status==200 ? await req.json() : await req.text()
    if(res.status === true){
        Swal.fire({
            icon: 'success',
            title: 'Datos actualizados',
            text: 'Los datos del usuario se han actualizado'
        })
    }
}

document.addEventListener('DOMContentLoaded', init_admin)