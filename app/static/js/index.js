window.onload = init

function init() {
    loadImages();
    $('.carousel-cursos').slick({
      slidesToShow: setCantSlides(),
      slidesToScroll: 1,
      autoplay: true,
      autoplaySpeed: 1400,
    });
}

function loadImages(){
    const barImgs = document.getElementsByClassName("barimg")
    for(let i=0; i <barImgs.length; i++){
        let img = barImgs[i].children[0]
        img.src = img.getAttribute("target")
    }
}

function setCantSlides(){
    const width = window.screen.width;

    const cantSlide = {
        640: 3,
        390: 2,
    }
    
    const maxWidth_ = Math.max(...Object.keys(cantSlide).map(n => Number(n)));
    if (width > maxWidth_) return 4
    
    let cant = 1;
    for(const maxWidth in cantSlide){
        if (width < maxWidth) cant = cantSlide[maxWidth]
    }
    return cant;
}

function loadPreguntas(){
    let temp = ''
    fetch('/get-preguntas')
    .then(res => res.json())
    .then(preguntas => {
        preguntas.forEach(post => {
            temp +=`<div class="container p-4">
                <div class="row form-control mb-2 d-flex">
                    <div class="w-1/6">
                        <div class="row text-center">
                            <div class="w-full">${post.votos}</div>
                            <div class="w-full">Votos</div>
                        </div>
                    </div>
                    <div class="w-5/6">
                        <div class="row dark:text-white">
                            <div class="w-full">
                                <a href="../pregunta/${post.uuid}" class="text-start mb-0" style="cursor: pointer; text-decoration: none;">${post.titulo}</a>
                            </div>
                            <div class="w-full">
                                <p class="text-end mb-1" data-bs-toggle="tooltip" data-bs-title="${post.fecha_edicion}">${post.fecha_edicion}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>`      
        });
        document.getElementById('preguntas').innerHTML = temp;
    })
}