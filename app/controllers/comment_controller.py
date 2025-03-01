from ..models.Comments import Comment
from ..database import comment_db

def save(comentario: Comment) -> Comment:
    return comment_db.save(comentario)

def eliminar(comentario: Comment) -> bool:
    return comment_db.eliminar(comentario)
