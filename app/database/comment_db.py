from ..models.Comments import Comment
from os import getenv

def save(comentario: Comment) -> Comment:
    comentario.save()
    return comentario

def eliminar(comentario: Comment) -> bool:
    try:
        comentario.delete().where(Comment.uuid == comentario.uuid)
        return True
    except: return False

