window.onload = init
let element_ant,  postTab_ant = null;
let inputImg, img_preview = null
let template_posts = null
let TOKEN = null

function init(){
    template_posts = document.getElementById("posts")
    element_ant = document.querySelector("button.active")
    TOKEN = document.getElementById("token").value
    inputImg = document.getElementById("fileperfil");

    initListeners()
    
    tipo = window.location.hash ? window.location.hash[1] : "p"
    if ("pri".includes(tipo)) getPosts(tipo == "i" ? "p" : tipo)
    else {
        const tag = location.hash.slice(1)
	    element_ant.classList.toggle("bg-dark")
    	element_ant.classList.toggle("active")
        const element = document.querySelector(`[target=${tag}]`)
        element.classList.toggle("bg-dark")
        element.classList.toggle("active")   
        loadView(tag)
	    element_ant = element
    }
}

function loadView(idView){
    location.hash = idView
    if(element_ant.getAttribute("class").split(" ").includes("active")) return;
    const view = document.getElementById(idView)
    document.getElementById(element_ant.getAttribute("target")).style.display = "none"
    view.style.display = "flex"
    if(view.getAttribute("fetch") == "true") {
        try{
            window[view.getAttribute("id")](view)
        }catch (error) {}
    }
}

function initListeners() {
    const triggerTabList = document.querySelectorAll('#myTab button')
    triggerTabList.forEach(triggerEl => {
      triggerEl.addEventListener('click', e => {
        e.preventDefault()
        let element = e.target
        element_ant.classList.toggle("bg-dark")
        if(element.tagName != "BUTTON") element = element.parentNode
        loadView(element.getAttribute("target"))
        element.classList.toggle("bg-dark")
        element_ant = element
      })
    })

    const formEdit = document.getElementById("formEdit")
    formEdit.addEventListener("submit", async (e)=>{
        e.preventDefault()

        const data = new FormData(formEdit)
        if(!not_empty(data)) return;
        if(inputImg.value) data.append("imagen", inputImg.files[0])

        const btnEdit = document.getElementById("editBtn")
        btnEdit.disabled = true
        
        const req = await fetch(`/user-update`, {
            method: "POST",
            body: data
        })
        const res = await req.json()
        const info = await res
        
        let titulo;
        if(info.status) titulo = "Datos actualiados correctamenete"
        else titulo =  info.msg ? info.msg : "Error del servidor"
        Swal.fire({
            icon: info.status ? 'success' : 'error',
            title: titulo,
            confirmButtonText: 'ok',
        }).then(res=>{
            if(info.status) location.reload()
        })
        btnEdit.disabled = false
    })

    img_preview = document.getElementById("img_preview")
    img_preview.addEventListener("click", ()=>document.getElementById("imgEdit").click());
    inputImg.addEventListener("change", previewImg)

    tabs = eventTabs(".posts")
    for(let tab of tabs){
        tab.addEventListener("changeTab", (e)=>{
            let attr = e.detail.hash
            location.hash = attr
            getPosts(attr[1])
        })
    }

    const btnDeletes = document.getElementsByClassName("delete")
    for(let i=0; i < btnDeletes.length; i++){
	btnDeletes[i].addEventListener("click", async (e)=>{
	    const element = e.target
	    let target = element.getAttribute("target")

	    fetch("/config-delete",{
		method: "DELETE",
		headers: {
		    "Content-Type": "application/json",
		    "X-CSRFToken": TOKEN
		},
		body: JSON.stringify({data: target})
	    })
	    .then(res=> res.json())
	    .then(data=> console.log(data))
	})
    }
}

function previewImg(e){
    e.preventDefault();
    const file = inputImg.files
    if(file || file.length){
        img_preview.src = URL.createObjectURL(file[0]);
    }
}

async function getPosts(tipo){
    loadder(template_posts)
    const req = await fetch(`/my-posts?tipo=${tipo}`)
    const res = await req.json()
    const data = await res
    if(data.data){
        print_posts(data.data, template_posts)
    } else template_posts.innerHTML = `No hay ${location.hash ? location.hash.slice(1) : "nada"} que mostrar`

}

async function transacciones(view){
    const req = await fetch('/get-transactions', {
        method: "POST",
        headers: {
            "X-CSRFToken": document.getElementById("token").value
        }
    })

    const res = await req.json()
    const data = await res
    
    let temp = ""
    if(data.total) temp += `<div class="col-3 monto">${data.monto}</div>`

    let compras = data.detalles.compras
    if(data.detalles.contratos.length){
	    let name_cols = ["Monto recibido", "fecha", "Id de venta", "Usuario cliente"]
	    const tableContratos = document.getElementById("contratos")
        if(tableContratos) tableContratos.innerHTML = createTable(name_cols, data.detalles.contratos)
    }
    if(compras.length) {
	    let name_cols = ["Monto pagado", "fecha", "Id de compra", "Usuario contratado"]
	    document.getElementById("tables").innerHTML = createTable(name_cols, compras)
    }
}

function createTable(cols, rows){
    const process_col = (cols)=> cols.map(col =>`<th>${col}</th>`)
    let rows_ = rows.map(row=> `<tr>${process_col(row).join("")}</tr>`)
    return `<table class="table table-dark table-hover">
	<thead>
	    <tr>
		${process_col(cols).join("")}
	    </tr>
	</thead>
	<tbody>
	    ${rows_.join(" ")}
	</tbody>
    </table>`
}
