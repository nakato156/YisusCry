from ..models.Comments import Comment
from .Model import Sentence
from os import getenv

def save(comentario: Comment) -> Comment:
    Sentence(comentario).save()
    return comentario

def eliminar(comentario: Comment) -> bool:
    try:
        Sentence(comentario).delete().where(("uuid", comentario.uuid))
        return True
    except: return False

def get_comments(comentario: Comment) -> list:
    table = getenv("BD_TABLE_USERS")
    select = f"SELECT {table}.username, &TABLE&.comentario, &TABLE&.fecha FROM `&TABLE&` INNER JOIN {table} ON &TABLE&.user_id = {table}.uuid"
    sentence = Sentence(comentario).free(select+" WHERE &TABLE&.post_id = {}", (comentario.post_id, ), results=True)
    return [Comment(comentario=comment, username=username, fecha=fecha) for username, comment, fecha in sentence]
