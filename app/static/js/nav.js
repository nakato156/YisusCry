window.onload = init

function init(){
    const formSearch = document.getElementById("search")
    const query = document.getElementById("searchQuery")
    formSearch.addEventListener('submit', (e)=>{
        e.preventDefault()
        const val = query.value.trim()
    })
}