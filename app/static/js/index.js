window.onload = init

function init() {
    loadImages();
    $('.carousel-cursos').slick({
      slidesToShow: 3,
      slidesToScroll: 1,
      autoplay: true,
      autoplaySpeed: 1400,
    });
}

function loadImages(){
    const barImgs = document.getElementsByClassName("barimg")
    console.log(barImgs)
    for(let i=0; i <barImgs.length; i++){
	let img = barImgs[i].children[0]
	img.src = img.getAttribute("target")
    }
}
