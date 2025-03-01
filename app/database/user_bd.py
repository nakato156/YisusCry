from ..models import User
from ..errors import UserNotFound
from os import getenv

def crear(user: User) -> User:
    user.save()
    return user
    
def eliminar(user: User) -> bool:
    try:
        user.delete().where(User.uuid == user.uuid)
        return True
    except Exception as e:
        print(e)
        return False

def eliminar_yisus(user: User) -> bool:
    try:
        user.delete().where(User.uuid == user.uuid)
        return True
    except: return False

def actualizar(user: User) -> User:
    user.update(user.get_object(ignore=('uuid', "password", "email", "fecha", "codigo"))).where(User.uuid == user.uuid)
    return user

def auth(user: User) -> User:
    data = user.get_or_none(User.username == user.username, User.password == user.password)
    if not data: raise UserNotFound("No se ha encontrado al usuario")
    return data

def get(user: User) -> User:
    ignore = ("role", "id_estado_cuenta", "ciclo")
    campos = user.get_object(exclude=ignore)
    res = user.get(**campos)
    if not res: raise UserNotFound
    return res

def get_one(user: User) -> User:
    return user.get(user.uuid == user.uuid, User.username == user.username)

def get_all() -> list:
    return [user for user in User.select().where(User.uuid != 1)]

def get_data(user: User) -> User:
    return user.get(User.uuid == user.uuid)

def count_posts(user: User) -> dict:
    table = getenv("BD_TABLE_POSTS")
    preguntas = user.raw("SELECT count(*) FROM " + table + " WHERE autor_id = {} AND tipo = 'p'", (user.uuid,))[0]
    respuestas = user.raw("SELECT count(*) FROM " + table + " WHERE autor_id = {} AND tipo = 'r'", (user.uuid,))[0]
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
