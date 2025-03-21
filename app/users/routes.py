from flask import Blueprint, render_template, session, request, abort, redirect
from app.functions.decorators import delete_csrf, valid_data_user, login_required
from app.controllers import post_controller, users_controller, comment_controller, contratos_controller
from app.functions.RoleManager import Role
from app.models.Contratos import Contrato
from app.models.Comments import Comment
from app.models.Posts import Post
from app.models import User
from uuid import uuid4
from os import getenv
import mercadopago
import requests
from pprint import pprint

user_routes = Blueprint('user_routes', __name__, template_folder="./templates/")

@user_routes.before_request
@login_required
def user_before_request():
    if session["user"]["id_estado_cuenta"] == 2:
        return render_template("suspendido.html")

@user_routes.get("/perfil")
def perfil():
    roles = Role(session["user"]["role"])
    return render_template("perfil.html", **session["user"], roles=roles)

@user_routes.get("/salir")
def salir():
    session.pop("user")
    return redirect("/")

@user_routes.get("/preguntar")
def preguntar():
    return render_template("formular.html", PUBLIC_KEY=getenv("PUBLIC_KEY"))

@user_routes.get("/my-posts")
def get_posts():
    user_uuid = str(session["user"].get("uuid"))
    user_posts = Post(autor_id=user_uuid, tipo=request.args.get("tipo", "p"))
    data_posts = post_controller.get_from_user(User(uuid=user_uuid), user_posts)
    return {"data": [data.get_object() for data in data_posts]}

@user_routes.post("/crear-pregunta")
@delete_csrf
def crear_post(data):
    data: dict = request.json
    data_post: dict = data.get("data_post")

    id_post = str(uuid4())
    try:
        nuevo_post = Post(uuid=id_post, autor_id=session["user"].get("uuid"), tipo ="p", **data_post)
        res = post_controller.crear(nuevo_post)
        return {"status": res, "id": id_post}
    except:
        return {"status": False}

@user_routes.post("/contratar")
def contratar():
    if not 'user' in session: abort(401)

    sdk = mercadopago.SDK(getenv("ACCESS_TOKEN"))
    
    data:dict = request.json
    data_payment = data.get("data_payment")
    data_user = data.get("data_user")
    
    yisus = User(uuid = data_user["id"])
    data_yisus = users_controller.get_data_yisus(yisus)

    if not data_yisus: abort(500)
    
    data_payment["transaction_amount"] = float(data_yisus["costo"])
    preference_response = sdk.payment().create(data_payment)
    response = preference_response.get("response")
    
    if response:
        monto = response.get("transaction_details")["net_received_amount"]
        contrato = Contrato(user_id=data_user["id"], client_id=session["user"]["uuid"], id=response["id"], monto=monto-(monto * .20))
        contratos_controller.save(contrato)
        return {"status": True}
    return {"status": False}

@user_routes.post("/actualizar-cuenta")
@valid_data_user(("username", "ciclo", "carrera"))
@delete_csrf
def update_user(data):
    user_:dict = session["user"]
    data["ciclo"] = int(data["ciclo"])

    if request.files.get("imagen"):
        res = requests.post(
            f'{getenv("HostStorageFiles")}/upload-file', 
            data = {
                'name': user_["username"]
            },
            files={
                'imagen': request.files.get("imagen").stream,
            },
            headers={
                'X-CSRFToken': getenv("STORAGE_TOKEN")
            }
        )
        if res.status_code != 200: 
            print(res.text)
            return {"status": False}
        print("uploading img...")

    if (user_["username"], user_["ciclo"], user_["carrera"]) == (data["username"], data["ciclo"], data["carrera"]):
        return {"status": True}

    data_user = User(**user_)

    users_controller.actualizar(data_user)

    user_.update(data)
    session["user"] = user_
    pprint(session["user"])
    return {"status": True}

@user_routes.post("/publicar-comentario")
def public_comentario():
    if not "user" in session: return abort(401)
    json:dict = request.json
    comentario:str = json.get("comentario")
    post_id:str = json.get("post_id")
    if not comentario.strip() or not post_id.strip(): return abort(400)
    comentario = Comment(comentario=comentario.strip(), user_id=session["user"]["uuid"], post_id=post_id.strip())
    comment_controller.save(comentario)
    return {"status": "test"}

@user_routes.post("/publicar-respuesta")
def public_respuesta():
    if not "user" in session: return abort(401)
    json = request.json
    print(json)
    # respuesta = json.get("respuesta")
    # comment_id = json.get("comment_id")
    # respuesta = Comment(respuesta=respuesta, user_id=session["user"]["uuid"], comment_id=comment_id)
    # comment_controller.save(respuesta)
    return {"status": "test"}

@user_routes.delete("/eliminar-cuenta")
def delete():
    try:
        users_controller.eliminar(User(**session["user"]))
        session.pop("user")
        return {"status": "test"}
    except:
        return {"status": False}
