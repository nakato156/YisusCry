let TOKEN_ = null
let formDataUser = null
let listaRoles = null
let btnActualizar = null

function confirmAlert(options, acceptCallback,  cancelCallback){
    Swal.fire(options)
    .then(async (result) => {
        if (result.isConfirmed){
            if (acceptCallback) acceptCallback()
        }
        else{
            if (cancelCallback) cancelCallback()
        }
    })
}

function init_admin(){
    const form_admin = document.getElementById("form_admin")
    TOKEN_ = document.getElementById("token").value
    btnActualizar = document.getElementById("updateUser")
    const btnEliminarUser = document.getElementById("deleteUser")
    const btnSupendUser = document.getElementById("suspendUser")
    const btnActivarUser = document.getElementById("activarUser")

    const masRoles = document.getElementById("masRoles")
    listaRoles = document.getElementById("listRoles")
    formDataUser = document.getElementById("form_update_user")
    
    masRoles.addEventListener("click", (e)=>addRole(e, listaRoles))
    btnSupendUser.addEventListener("click", suspendUser)
    btnEliminarUser.addEventListener("click", deleteUser)
    btnActivarUser.addEventListener("click", activarUser)

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

            const btnAction = info_user.id_estado_cuenta === 1 ? btnSupendUser : btnActivarUser;
            const activateVisible = info_user.id_estado_cuenta !== 1;

            btnActivarUser.parentElement.classList.toggle("d-none", !activateVisible);
            btnSupendUser.parentElement.classList.toggle("d-none", activateVisible);

            Object.values(formDataUser.elements).forEach(element => {
                let name = element.name
                element.value = (info_user && info_user[name]) ? info_user[name] : "---"
            })

            let lista, mas_roles = ""

            btnActualizar.disabled = !info_user.uuid
            btnEliminarUser.disabled = !info_user.uuid
            btnAction.disabled = !info_user.uuid

            if(info_user.role){
                lista = crearTemplateLista(Object.values(info_user.role), true)
                mas_roles = crearTemplateLista(Object.values(info_user.masRoles))
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

function suspendUser(e){
    e.preventDefault()
    const options = {
        title: '¿Estás seguro?',
        text: "Seguro que quieres suspener al usuario",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, suspender!'
    }
    acceptCallback = async () => {
        const req = await fetch(`/admin/state-account-user`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': TOKEN_
            },
            body: JSON.stringify({uuid: formDataUser.uuid.value})
        })

        const res = await req.status==200 ? await req.json() : await req.text()
        if(res.status === true)
            Swal.fire('Suspendido!', 'El usuario se ha suspendido', 'success')
        else 
            Swal.fire('Error!', 'No se ha podido suspender al usuario, intentelo de nuevo', 'error')
    }
    confirmAlert(options, acceptCallback, null)
}

function activarUser(e){
    e.preventDefault()
    const options = {
        title: '¿Estás seguro?',
        text: "Quieres activar al usuario?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, activar!'
    }
    const acceptCallback = async () =>{
        const req = await fetch(`/admin/state-account-user`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': TOKEN_
            },
            body: JSON.stringify({
                uuid: formDataUser.uuid.value,
                reactivar: true
            })
        })
        
        const res = await req.status==200 ? await req.json() : await req.text()
        if(res.status === true)
            Swal.fire('Activado!', 'La cuenta del usuario ha sido activada', 'success')
        else 
            Swal.fire('Error!', 'No se ha podido activar al usuario, intentelo de nuevo', 'error')   
    }
    confirmAlert(options, acceptCallback)
}

function deleteUser(e){
    e.preventDefault()
    const options = {
        title: 'Seguro que quieres eliminar al usuario?',
        text: "Esta acción es irreversible. ¿Estás seguro?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, eliminar!'
    }
    acceptCallback = async () => {
        const req = await fetch(`/admin/delete-user`, {
            method: "DELETE",
            headers: {
                'X-CSRFToken': TOKEN_
            }
        })

        const res = await req.status==200 ? await req.json() : await req.text()
        if(res.status === true)
            Swal.fire('Eliminado!', 'El usuario se ha eliminado', 'success')
    }
    confirmAlert(options, acceptCallback, null)
}

document.addEventListener('DOMContentLoaded', init_admin)