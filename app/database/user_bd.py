from ..models.Users import User
from .Model import Sentence
from os import getenv

def crear(user: User) -> User:
    Sentence(user).save(user.get_object())
    return user
    
def eliminar(user: User) -> bool:
    user_id = user.uuid
    try:
        Sentence(user).delete().where(('uuid', user.uuid)).execute()
        return True
    except Exception as e:
        print(e)
        return False

def actualizar(user: User) -> User:
    Sentence(user).update(user.get_object(ignore=("password", "email", "fecha", "codigo"))).execute()
    return user

def auth(user: User) -> User:
    data = Sentence(user).select().where(("username", user.username)).where(("password", user.password)).execute()
    return User(*data)

def get_one(user: User) -> User:
    data = Sentence(user).select().where(("uuid", user.uuid)).execute()
    return User(*data)

def get_all() -> list[User]:
    return [User(*user) for user in Sentence(User()).select().execute(select_one=False)]

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