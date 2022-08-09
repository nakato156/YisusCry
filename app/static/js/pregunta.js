window.onload = init
let comentario = null;
let zona_comentarios = null;

function init(){
    const elemento = document.getElementById("contenido");
    zona_comentarios = document.getElementById("comentariosZ")
    const md = new MD(elemento)
    md.parse()

    comentario = document.getElementById("comentario")
    localStorage.setItem("bbss", comentario.getAttribute("bs"))
    comentario.addEventListener("click", (e)=>{
        if(localStorage.getItem("bbss").toLowerCase() == "false") return alert("Debes iniciar sesion")
        else createBox()
    })
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