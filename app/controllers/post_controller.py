from app.models import User, Post, Comment
from ..database import post_bd
from typing import List
from typing import Tuple

def crear(post: Post) -> Post:
    post_bd.crear(post)
    return post

def eliminar(post: Post) -> bool:
    return post_bd.eliminar(post)

def actualizar(post: Post) -> Post:
    post_bd.actualizar(Post)
    return post

def get(limit: int) -> List[Post]:
    return post_bd.get(limit)

def get_one(post: Post) -> Post:
    return post_bd.get_one(post)

def get_recent(limit: int) -> List[Post]:
    return post_bd.get_recent(limit)

def get_all(tipo: str = "") -> List[Post]:
    return post_bd.get_all(tipo)

def get_from_que(post: Post) -> List[Post]:
    return post_bd.get_form_ques(post)

def get_from_user(user:User, post: Post) -> List[Post]:
    return post_bd.get_from_user(user, post)

def get_post_with_comments(post_id:str) -> Tuple[Post, List[Comment]]:
    return post_bd.get_post_with_comments(post_id)