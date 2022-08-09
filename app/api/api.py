from flask import Blueprint, request
from app.functions.decorators import save_logger
from app.models import Users
from app.database import Model

api = Blueprint("api", __name__, url_prefix="/api/v1/")

@api.get("/search/<string:query>")
@save_logger
def search(query: str):
    key = request.args.get("k")
    if key == "p":
        pass
    elif key == "u":
        res_user = Users.User()
        sentence = Model.Sentence(res_user).select('uuid, username, carrera, ciclo').where(("username", "LIKE", f"%{query}%"))
        return {
            "status": True,
            "info": [dict(zip( ('id', 'username', 'carrera', 'ciclo') ,res)) for res in res_user.execute(sentence, select_one=False)]
        }
    return {"status": True}
