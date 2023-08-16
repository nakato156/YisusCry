window.onload = init
let comentario = null;
let zona_comentarios = null, boxRespuesta = null;
const editores = {}

function generarIdAleatorio(longitud) {
    let caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let id = '';

    for (let i = 0; i < longitud; i++) {
      let indice = Math.floor(Math.random() * caracteres.length);
      id += caracteres.charAt(indice);
    }

    return id;
}

function init(){
    boxRespuesta = document.getElementById("boxRespuesta")
    zona_comentarios = document.getElementById("comentariosZ")
    const btnAddCode = document.getElementById("addCode")
    const btnAddTexto = document.getElementById("addTexto")
    const btnPublicarResp = document.getElementById("btnPublicarRespuesta")
    const elemento = document.getElementById("contenido");
    const md = new MD(elemento)
    md.parse()

    comentario = document.getElementById("comentario")
    localStorage.setItem("bbss", comentario.getAttribute("bs"))
    comentario.addEventListener("click", (e)=>{
        if(localStorage.getItem("bbss").toLowerCase() == "false") return Swal.fire({icon:"warning", title:"Debes iniciar sesion"})
        else createBox()
    })
    btnAddCode.addEventListener("click", addCode)
    btnAddTexto.addEventListener("click", addTexto)
    btnPublicarResp.addEventListener("click", publicar_respuesta)
}

function crearDivRespuesta(id){
    const div = document.createElement("div")
    div.id = id || generarIdAleatorio(10)
    div.classList.add("estilosEditor")
    div.innerHTML = `<div class="icon">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
    </div>`
    div.getElementsByClassName("icon")[0].addEventListener("click", ()=>{
        if(editores[div.id]) delete editores[div.id]
        div.remove()
    })
    return div
}

function addCode(){
    const div = crearDivRespuesta()
    boxRespuesta.appendChild(div)
    require(["vs/editor/editor.main"], function () {
        let editor = monaco.editor.create(div, {
            value: "",
            language: 'javascript',
            theme: 'vs-dark'
        });
        editores[div.id] = editor
    });
}

function addTexto(){
    const div = crearDivRespuesta()
    div.setAttribute("data", "texto")
    const divTextArea = document.createElement("div")
    divTextArea.classList.add("form-outline", "p-4")
    const textarea = document.createElement("textarea")
    textarea.classList.add("form-control")
    textarea.rows = 10
    divTextArea.appendChild(textarea)
    div.appendChild(divTextArea)
    boxRespuesta.appendChild(div)
}

function createBox(){
    let element = `
        <div class="col">
            <textarea class="form-control" style="width:90%; resize: none;" id="BoxComment" placeholder="Escribe tu comentario"></textarea>
        <div>
        <div class="col-2"><p style="cursor: pointer;" onclick="">Enviar</p></div>`
    comentario.parentNode.parentNode.innerHTML = element;
    comentario = document.getElementById("BoxComment")
    comentario.addEventListener("keyup", publicar_comentario)
}

function publicar(contenido){
    console.log(contenido)
    let hora = new Date()
    zona_comentarios.innerHTML += `
    <div class="col-5 comentario mb-1" style="border-bottom: 1px solid #ccc;">
        <div class="row contenido"><p>${contenido}</p></div>
        <div class="row info"><p>{username} - ${hora.getHours()}:${hora.getMinutes()}</p></div>
    </div>
    `
    comentario.disabled = false;
    comentario.parentNode.style.display = "none"
}

async function publicar_comentario(e){
    if(e.key != "Enter" || e.code != "Enter") return;
    comentario.disabled = true;
    const req = await fetch("/public-comment", {
        method: "POST",
        body: JSON.stringify({
            "comentario": comentario.value,
            "post_id": location.href.split("/").slice(-1)[0]
        }),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": comentario.getAttribute("data")
        }
    })
    const res = await req
    if(res.satus == 200 ){
        publicar(document.getElementById("BoxComment").value)
    }else if(res.status == 401) window.href = "../../login"

}

function checkRespuesta(){

}

function serializarRespuesta(){
    const boxRespuesta = document.getElementById("boxRespuesta")
    if(!boxRespuesta) return false
    const children = boxRespuesta.children
    let respuesta = []
    for(element of children){
        if(editores[element.id]){
            if(!editores[element.id].getValue().trim()) continue
            respuesta.push({tipo:"code", val: editores[element.id].getValue()})
        }
        else if (element.getAttribute("data") == "texto"){
            const textarea = element.getElementsByTagName("textarea")[0]
            if(!textarea.value.trim()) continue
            respuesta.push({tipo:"texto", val: textarea})
        }
    }
    return respuesta
}

function checkRespuesta(respuesta){
    if(respuesta.length == 0) {
        Swal.fire({icon: "error", title: "Debe escribir algo en la respuesta"})
        return false
    }
    const totalCaracteres = respuesta.reduce((acumulador, objeto) => {
        const caracteresNoVacios = objeto.val.split('').filter(caracter => caracter !== ' ').length;
        return acumulador + caracteresNoVacios;
    }, 0);
    if(totalCaracteres <= 180){
        Swal.fire({icon: "error", title: "La respuesta es muy corta"})
        return false
    }
    return true
}

async function publicar_respuesta(e){
    const respuesta = serializarRespuesta()
    const respuestaValida = checkRespuesta(respuesta)
    if(!respuestaValida) return;
    console.log(respuesta)
    fetch('/publicar/respuesta', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(respuesta)
    })
    .then(res => res.text())
    .then(data => console.log(data))
    .catch(err => console.log("erro:",err))
}