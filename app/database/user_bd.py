from ..models.Users import User
from .Model import Sentence
from ..errors import UserNotFound
from os import getenv

def crear(user: User) -> User:
    Sentence(user).save()
    return user
    
def eliminar(user: User) -> bool:
    try:
        Sentence(user).delete().where(('uuid', user.uuid)).execute()
        return True
    except Exception as e:
        print(e)
        return False

def eliminar_yisus(user: User) -> bool:
    try:
        Sentence(user).delete().where(('uuid', user.uuid)).execute()
        Sentence(user).update({"user_id": "1"}).where(('user_id', user.uuid)).execute()
        return True
    except: return False

def actualizar(user: User) -> User:
    sentence = Sentence(user).update(user.get_object(ignore=('uuid', "password", "email", "fecha", "codigo"))).where(('uuid', user.uuid))
    sentence.execute()
    return user

def auth(user: User) -> User:
    data = Sentence(user).select().where(("username", user.username)).where(("password", user.password)).execute()
    return User(*data)

def get(user: User) -> User:
    data = Sentence(user).select()
    campos = user.get_object(("role", "edad", "ciclo", "carrera", "info"))
    for k,v in campos.items():
        if v: data.where((k, v))
    res = data.execute()
    if not res: raise UserNotFound
    return User(*res)


def get_one(user: User) -> User:
    data = Sentence(user).select().where(("uuid", user.uuid)).where(("username", user.username), "OR").execute()
    return User(*data)

def get_all() -> list:
    return [User(*user) for user in Sentence(User()).select().where(('uuid', "!=", "1")).execute(select_one=False)]

def get_data(user: User) -> User:
    data = Sentence(user).select().where(('uuid', user.uuid)).execute()
    return User(*data)

def count_posts(user: User) -> dict:
    table = getenv("BD_TABLE_POSTS")
    preguntas = Sentence(user).free("SELECT count(*) FROM " + table + " WHERE autor_id = {} AND tipo = 'p'", (user.uuid,), results=True)[0]
    respuestas = Sentence(user).free("SELECT count(*) FROM " + table + " WHERE autor_id = {} AND tipo = 'r'", (user.uuid,), results=True)[0]
    return {
        "preguntas": preguntas[0],
        "respuestas": respuestas[0]
    }

def get_data_yisus(user: User) -> dict:
    table = getenv("BD_TABLE_CONFIG_ACCOUNT_Y")
    data = Sentence(user).free("SELECT * FROM "+table+" WHERE user_id = {}", (user.uuid, ), results=True)
    if data:
        return dict(zip(("uuid", "costo", "nro_cuenta"), data[0]))
    return {}

def get_transacciones(user: User) -> dict:
    table = getenv("BD_TABLE_CUENTAS_USERS")
    table_users = getattr(user, "__table")
    
    select = f"SELECT {table}.monto, {table}.fecha, {table}.id, {table_users}.username FROM {table} INNER JOIN {table_users}"
    
    on = f" ON {table_users}.uuid = {table}.user_id"
    compras = Sentence(user).free(select + on +" WHERE client_id = {} ORDER BY fecha", (user.uuid,), results=True)
    on = f" ON {table_users}.uuid = {table}.client_id"
    ganancias = Sentence(user).free(select + on +" WHERE user_id = {} ORDER BY fecha", (user.uuid,), results=True)
    print(ganancias)

    return {"detalles": {"compras": compras, "contratos": ganancias}, "monto": sum(info[0] for info in ganancias)}
