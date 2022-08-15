window.onload = init
let token, user_id, template = null;
let MODAL = null
let formPago = null

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
    
    document.getElementById("denunciar").addEventListener("click", (e)=>{
	    const id = window.location.href.split("/").slice(-1)[0]
	    window.location.href = `../../denuncia?id=${id}`
    })
    const contratarBtn = document.getElementById("contratar")
    
    MODAL = new bootstrap.Modal("#ModalPago")

    if(contratarBtn){
	contratarBtn.addEventListener("click", (e)=>{
	    if(e.target.getAttribute("bs").toLowerCase() == "true") MODAL.show()
	    else window.location.href = `../../login`
	})
    }

    const cardForm = mp.cardForm({
              amount: "5.5",
              iframe: true,
              form: {
                id: "form-checkout",
                cardNumber: {
                  id: "form-checkout__cardNumber",
                  placeholder: "Numero de tarjeta",
                },
                expirationDate: {
                  id: "form-checkout__expirationDate",
                  placeholder: "MM/YY",
                },
                securityCode: {
                  id: "form-checkout__securityCode",
                  placeholder: "Código de seguridad",
                  class: "form-control",
                },
                cardholderName: {
                  id: "form-checkout__cardholderName",
                  placeholder: "Titular de la tarjeta",
                },
                issuer: {
                  id: "form-checkout__issuer",
                  placeholder: "Banco emisor",
                },
                installments: {
                  id: "form-checkout__installments",
                  placeholder: "Cuotas",
                },
                identificationType: {
                  id: "form-checkout__identificationType",
                  placeholder: "Tipo de documento",
                },
                identificationNumber: {
                  id: "form-checkout__identificationNumber",
                  placeholder: "Número del documento",
                },
                cardholderEmail: {
                  id: "form-checkout__cardholderEmail",
                  placeholder: "E-mail",
                },
              },
              callbacks: {
                onFormMounted: error => {
                  if (error) return console.warn("Form Mounted handling error: ", error);
                },
                onSubmit: event => {
                  event.preventDefault();

                  const {
                    paymentMethodId: payment_method_id,
                    issuerId: issuer_id,
                    cardholderEmail: email,
                    amount,
                    token,
                    installments,
                    identificationNumber,
                    identificationType,
                  } = cardForm.getCardFormData();
		  
		  // if(formPago==null) return;
                  fetch("/contratar", {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                        "X-CSRFToken": document.getElementById("datacsrxf").value
                    },
                    body: JSON.stringify({
			"data_user": {
			    "id": window.location.href.split("/").slice(-1)[0]
			},
			"data_payment": {
			    token,
			    issuer_id,
			    payment_method_id,
			    transaction_amount: Number(amount),
			    installments: Number(installments),
			    payer: {
				email,
				identification: {
				    type: identificationType,
				    number: identificationNumber,
				},
			    },
			}
                    }),
                  })
                  .then(req => req.json())
                  .then(res => {
		      console.log(res)
		    if(res.status == 401){
			window.location.href = "../../login"
		    }else if(res.status){
			MODAL.hide()
                        // window.location.href = `../pregunta/${res.id}`
                    }else{
                        alert("Ha ocurrido un error al publicar la pregunta o al procesar el pago")
                    }
                  });
                },
                onFetching: (resource) => {
                  console.log("Fetching resource: ", resource);

                  const progressBar = document.querySelector(".progress-bar");
                  progressBar.removeAttribute("value");

                  return () => {
                    progressBar.setAttribute("value", "0");
                  };
                }
            },
        });
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
