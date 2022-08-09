window.onload = init

function init(){
    const pregunta = document.getElementById("formPregunta")
    const dynamicDivs = document.querySelectorAll(".containerPago")
    const MODAL = new bootstrap.Modal("#ModalPago")

    pregunta.addEventListener("submit", async e => {
        e.preventDefault()
        const data = new FormData(pregunta)

        const values = Object.fromEntries(data.entries())
        delete values.csrf_token

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
                  console.log("Form mounted");
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

                  fetch("/crear-pregunta", {
                    method: "POST",
                    headers: {
                      "Content-Type": "application/json",
                        "X-CSRFToken": new FormData(document.getElementById("formPregunta")).get("csrf_token")
                    },
                    body: JSON.stringify({
                      "data_post": values,
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
                    if(res.status){
                        MODAL.hide()
                        window.location.href = `../pregunta/${res.id}`
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
        setTimeout(()=> MODAL.show(), 1000)
    })
}

