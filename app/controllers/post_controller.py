from ..models.Posts import Post
from ..database import post_bd

def crear(post: Post) -> Post:
    post_bd.crear(post)
    return post

def eliminar(post: Post) -> bool:
    return post_bd.eliminar(post)

def actualizar(post: Post) -> Post:
    post_bd.actualizar(Post)
    return post

def get_one(post: Post) -> Post:
    return post_bd.get_one(post)

def get_all(tipo: str = "") -> list[Post]:
    return post_bd.get_all(tipo)

def get_from_que(post: Post) -> list[Post]:
    return post_bd.get_form_ques(post)

def get_from_user(post: Post) -> list[Post]:
    return post_bd.get_from_user(post)