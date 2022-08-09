from app.database.Model import Sentence
from app.controllers import users_controller

def exist(modelo) -> bool:
    sentence = Sentence(modelo).select().where(tuple(modelo.get_objct()))
    return not not sentence.execute()