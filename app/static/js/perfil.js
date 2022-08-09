window.onload = init
var element_ant,  postTab_ant = null;
let template_posts = null
const HOST = window.location.hostname != "localhost" ? window.location.host : ""

function init(){
    template_posts = document.getElementById("posts")
    initListeners()
    tipo = window.location.hash ? window.location.hash[1] : "p"
    if (["p","r"].includes(tipo)) getPosts(tipo)
    else {
        const tag = location.hash.slice(1)
        element_ant.classList.toggle("bg-dark")
        element_ant.classList.toggle("active")
        const element = document.querySelectorAll(`[target=${tag}]`)[0]
        element.classList.toggle("bg-dark")
        element.classList.toggle("active")
        loadView(tag)
    }
}

function loadView(idView){
    location.hash = idView
    if(element_ant.getAttribute("class").split(" ").includes("active")) return
    const view = document.getElementById(idView)
    document.getElementById(element_ant.getAttribute("target")).style.display = "none"
    view.style.display = "flex"
}

function initListeners() {
    const triggerTabList = document.querySelectorAll('#myTab button')
    triggerTabList.forEach(triggerEl => {
      element_ant = element_ant ? element_ant : triggerEl
      triggerEl.addEventListener('click', e => {
        e.preventDefault()
        e.stopPropagation()
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
        const btnEdit = document.getElementById("editBtn")
        btnEdit.disabled = true
        const req = await fetch(`${HOST}/user-update`, {
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

    tabs = eventTabs(".posts")
    for(let tab of tabs){
        tab.addEventListener("changeTab", (e)=>{
            let attr = e.detail.hash
            location.hash = attr
            getPosts(attr[1])
        })
    }
}

async function getPosts(tipo){
    loadder(template_posts)
    const req = await fetch(`${HOST}/my-posts?tipo=${tipo}`)
    const res = await req.json()
    const data = await res
    if(data.data){
        print_posts(data.data, template_posts)
    } else template_posts.innerHTML = `No hay ${location.hash ? location.hash.slice(1) : "nada"} que mostrar`

}