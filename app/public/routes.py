from flask import Blueprint, render_template, session, request, jsonify
from app.functions.decorators import delete_csrf, valid_data_user, save_logger, not_login
from app.controllers import users_controller, post_controller, comment_controller
from app.models.Comments import Comment
from app.models import User
from app.models.Posts import Post
from os import getenv
from functools import reduce

public_routes = Blueprint("public_routes", __name__, template_folder="./templates")

@public_routes.get("/")
def index():
    cursos = ["progra1", "calculo1", "calculo2", "progra2", "algoritmos", "mate_discreta"]
    return render_template("index.html", cursos = cursos, users = users_controller.get_all())

@public_routes.get('/get-preguntas')
def get_preguntas():
    return jsonify([post.get_object(exclude=('contenido', 'referencia', "autor_id", "fecha_publicado"), extra_attrs=["votos"]) for post in post_controller.get(3)])

@public_routes.get("/registro")
@not_login
def registro():
    return render_template("registro.html")

@public_routes.post("/registro")
@not_login
@valid_data_user(("username", "password", "email", "codigo"))
@delete_csrf
@save_logger
def post_registro(data):
    data["edad"] = int(data["edad"])
    data["ciclo"] = int(data["ciclo"])
    new_user = User(**data)
    new_user = users_controller.crear(new_user)
    if new_user:
        data_user = users_controller.get_one(new_user)
        session["user"] = data_user.get_object(exclude=("password",))
        res = {"status": True}
    else:
        res = {"status": False, "error": "Datos ya registrados :c"}
    return res

@public_routes.get("/login")
@not_login
def login():
    return render_template("login.html")

@public_routes.post("/login")
@not_login
@valid_data_user()
@delete_csrf
def login_user(data):
    data_user = User(**data)
    try:
        data = users_controller.auth(data_user)
        if data:
            session["user"] = users_controller.get_one(data).get_object(exclude=('password', ))
            return {"status": True}
    except Exception as e: 
        print(e)
        return {"status": False}

@public_routes.get("/preguntas")
def preguntas():
    return render_template("preguntas.html", preguntas=(post.get_object() for post in post_controller.get_all('p')))

@public_routes.get("/pregunta/<string:id>")
def pregunta(id: str):
    post = Post(uuid=id)
    data_post, data_comments = post_controller.get_post_with_comments(post.uuid)

    if "user" in session:
        data_autor = users_controller.get(User(uuid=data_post.autor_id)).get_object(exclude=("edad", "ciclo", "codigo", "email"))
    else: data_autor = {"username": "desconocido"}

    respuestas = (post_.get_object() for post_ in post_controller.get_from_que(post))
    comentarios = (comment.get_object() for comment in data_comments)
    
    info_votos = ({"votos_up": vote.votos_up, "votos_dn": vote.votos_dn} for vote in data_post.Votos)
    votos_dict = reduce(lambda resumen, voto: {"votos_up": resumen.get("votos_up", 0) + voto["votos_up"], "votos_dn": resumen.get("votos_dn", 0) + voto["votos_dn"]}, info_votos, {})
    votos = {
        "votos": votos_dict["votos_up"] + votos_dict["votos_dn"],
        "votos_up": votos_dict["votos_up"],
        "votos_dn": votos_dict["votos_dn"]
    }
    
    return render_template("pregunta.html", data_autor=data_autor, respuestas=respuestas, comentarios=comentarios, **data_post.get_object(), **votos)

@public_routes.post("/get-posts/<string:user_id>")
def get_posts(user_id: str):
    tipo = request.args.get("tipo")
    post = Post(autor_id=user_id, tipo=tipo)
    return {"data": [post.get_object() for post in post_controller.get_from_user(post)]}

@public_routes.get("/user/<string:id>")
def get_user(id: str):
    user = User(uuid = id)
    posts = users_controller.count_posts(user)
    return render_template("user.html", **users_controller.get_one(user).get_object(exclude=('password', 'fecha'), convert=True), **posts, PUBLIC_KEY=getenv("PUBLIC_KEY"))

@public_routes.get("/denuncia")
def denuncia():
    id = request.args.get("id")
    if not id: return "<h1>No se ha seleccionado algún usuario</h1><br><a href='../'>regresar</a>"
    return render_template("denuncia.html", id=id)
