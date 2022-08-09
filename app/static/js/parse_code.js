class MD {
    constructor (element) {
        this.element = element
    }

    parse(){
        let temp  = "<div class='col'>"
        let contenido = this.element.innerHTML
        let begin = 1;
        for(let linea of contenido.split("\n")){
            if(linea.includes("```")){
                temp+= begin ? "<pre><code>" : "</pre></code>"
                begin = !begin
            }else {
                temp+= !begin ? linea : `<p>${linea}</p>`
            }
        }
        temp+"</div>"
        this.element.innerHTML = temp
    }
}