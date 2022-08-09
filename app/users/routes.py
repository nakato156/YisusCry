from flask import Blueprint, render_template, session, request, abort
from app.functions.decorators import delete_csrf, valid_data_user, login_required
from app.controllers import post_controller, users_controller, comment_controller
from app.models.Comments import Comment
from app.models.Posts import Post
from app.models.Users import User
from uuid import uuid4
from os import getenv
import mercadopago

user_routes = Blueprint('user_routes', __name__, template_folder="./templates/")

@user_routes.get("/perfil")
@login_required
def perfil():
    return render_template("perfil.html", **session["user"])

@user_routes.get("/preguntar")
@login_required
def preguntar():
    return render_template("formular.html", PUBLIC_KEY=getenv("PUBLIC_KEY"))

@user_routes.get("/my-posts")
@login_required
def get_posts():
    user_posts = Post(autor_id=session["user"].get("uuid"), tipo=request.args.get("tipo", "P"))
    data_posts = post_controller.get_from_user(user_posts)
    return {"data": [data.get_object() for data in data_posts]}

@user_routes.post("/crear-pregunta")
@login_required
@delete_csrf
def crear_post(data):
    data: dict = request.json
    data_post: dict = data.get("data_post")

    id_post = str(uuid4())
    sdk = mercadopago.SDK(getenv("ACCESS_TOKEN"))
    nuevo_post = Post(uuid=id_post, autor_id=session["user"].get("uuid"), tipo ="p", **data_post)

    data_payment: dict = data.get("data_payment")
    data_payment.update(nuevo_post.data_pago())

    preference_response = sdk.payment().create(data_payment)
    preference = preference_response["response"]

    if preference["status"].lower() == "approved":
        res = post_controller.crear(nuevo_post)
        return {"status": True, "id": id_post}
    return {"status": False}

@user_routes.post("/user-update")
@valid_data_user(("username", "ciclo", "carrera"))
@delete_csrf
def update_user(data):
    user_ = session["user"]
    data["ciclo"] = int(data["ciclo"])

    if (user_["username"], user_["ciclo"], user_["carrera"]) == (data["username"], data["ciclo"], data["carrera"]):
        return {"status": True}

    data_user = User(**user_)

    if request.files.get("perfil"):
        img = request.files.get("perfil").stream
        data_user.perfil = img

    users_controller.actualizar(data_user)

    user_.update(data)
    session["user"] = user_
    return {"status": True}

@user_routes.post("/public-comment")
def public_comentario():
    if not "user" in session: return abort(401)
    json = request.json
    comentario = json.get("comentario")
    post_id = json.get("post_id")
    comentario = Comment(comentario=comentario, user_id=session["user"]["uuid"], post_id=post_id)
    comment_controller.save(comentario)
    return {"status": "test"}