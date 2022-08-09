window.__currentTab__ = null

function eventTabs(selector){
    const postsTabs = document.querySelectorAll(selector)
    postsTabs.forEach(tabPost => {
        if(!window.__currentTab__) window.__currentTab__ = tabPost
        tabPost.addEventListener("click", e => {
            if(window.__currentTab__ == e.target || window.__currentTab__ == e.target.parentNode) return;
            const element = e.target
            window.__currentTab__ = element
            element.dispatchEvent(new CustomEvent("changeTab", {
                bubbles: true,
                detail: {
                    element: e.target,
                    hash: e.target.getAttribute("href")
                }
            }))
        })
    })
    return postsTabs;
}

function parse_date(fecha){
    fecha = new Date(fecha).toLocaleString().substring().trim()
    return fecha.substring(0, fecha.length-3)
}

function loadder(template) {
    template.innerHTML = `
    <div class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>`
}

function print_posts(data, template){
    let temp = ""
    data.forEach(post => {
        temp += `
            <div class="row form-control mb-2 d-flex">
                <div class="col-2">
                    <div class="row text-center">
                        <div class="col-12">${post.votos}</div>
                        <div class="col-12">Votos</div>
                    </div>
                </div>
                <div class="col-10">
                    <div class="row">
                        <div class="col-12">
                            <a href="../pregunta/${post.uuid}" class="text-start mb-0" style="cursor: pointer; text-decoration: none; color: black;">${post.titulo}</a>
                        </div>
                        <div class="col-12">
                           <p class="text-end mb-1" data-bs-toggle="tooltip" data-bs-title="${post.fecha_edicion}">${parse_date(post.fecha_edicion)}</p>
                        </div>
                    </div>
                </div>
            </div>`
    })
    template.innerHTML = temp
}