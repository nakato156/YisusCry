from flask import Blueprint, request
from app.models import User
from app.functions.decorators import login_required
from app.controllers import users_controller
from app.functions.RoleManager import Role
from app.errors import UserNotFound

admin_routes = Blueprint("admin_routes", __name__, template_folder="./templates", url_prefix="/admin")

@admin_routes.post("/info-user")
@login_required
def info_user():
    data: dict = request.form.to_dict()
    criterio = data.pop("criterio")

    user_query = User(**{criterio: data.get("query")})
    try:
        res = users_controller.get(user_query)
        res = res.get_object(exclude=("password", "info", "fecha"))
        res["role"] = Role(res["role"]).roles
        res["masRoles"] = list(set(Role.ROLES.values()) - set(res["role"].values()) )
    except UserNotFound: res = {}
    return {"status": True, "info": res}

@admin_routes.put("/user-update")
@login_required
def update_user():
    data = request.form.to_dict()
    print(data)
    roles = Role.convert(set(data["roles"].split(",")))
    user = User(uuid=data["uuid"], username=data["username"], role=roles)
    users_controller.actualizar(user)
    return {"status": True}

@admin_routes.put("/state-account-user")
@login_required
def suspend_user():
    data:dict = request.json
    estado:int = 1 if data.get("reactivar") else 2
    try:
        user = User(uuid=data["uuid"], id_estado_cuenta=estado)
        users_controller.actualizar(user)
        return {"status": True}
    except Exception as e:
        return {"status": False}