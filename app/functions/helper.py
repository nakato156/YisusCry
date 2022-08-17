from app.database.Model import Sentence
from .RoleManager import Role

def exist(modelo) -> bool:
    sentence = Sentence(modelo).select().where(tuple(modelo.get_objct()))
    return not not sentence.execute()

def has_role(hash_: str, rol: str):
    roles = Role(hash_)
    return roles.has(rol)