window.onload = init

function init() {
    $('.carousel-cursos').slick({
      slidesToShow: 3,
      slidesToScroll: 1,
      autoplay: true,
      autoplaySpeed: 1400,
    });
}

function loadImages(){
	const barImgs = document.getElementsByClassName("barimg")
	for(let i; i <barImgs.length; i++){
		// img.src = ''
	}
}
