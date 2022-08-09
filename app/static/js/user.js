window.onload = init
let token, user_id, template = null;

function init(){
    token = document.getElementById("csrf_token").value
    template = document.getElementById("posts")
    user_id = window.location.href.split("/").slice(-1)
    let tabs = eventTabs(".posts")
    for(let tab of tabs){
        tab.addEventListener("changeTab", (e)=>{
            get_posts(e.detail.hash.slice(1,2))
        })
    }
    get_posts("p")
}

async function get_posts(tipo){
    loadder(template)
    const req = await fetch(`/get-posts/${user_id}?tipo=${tipo}`, {
        method: "POST",
        headers: {
            "X-CSRFToken": token
        }
    })
    const res  = await req.json()
    const data = await res
    print_posts(data["data"], template)
}