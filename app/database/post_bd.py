from ..models.Posts import Post
from .Model import Sentence
from typing import List

def crear(post: Post) -> Post:
    Sentence(post).save()
    return post

def eliminar(post: Post) -> bool:
    try:
        Sentence(post).delete().where(('uuid', post.uuid))
        return True
    except: return False

def actualizar(post: Post) -> Post:
    Sentence(post).update(post.get_object()).where(("uuid", post.uuid)).execute()
    return post

def get(limit: int) -> List[Post]:
    sentence = Sentence(Post()).select().limit(limit)
    return [Post(*post) for post in sentence.execute(select_one=False)]

def get_one(post: Post) -> Post:
    sentence = Sentence(post).select().where(("uuid", post.uuid))
    return Post(*sentence.execute())

def get_all(tipo: str = "") -> list:
    sentence = Sentence(Post()).select()
    if tipo: sentence = sentence.where(("tipo", tipo))
    return [Post(*post) for post in sentence.execute(select_one=False)]

def get_form_ques(post: Post) -> list:
    sentence = Sentence(post).select().where(('referencia', post.uuid)).where(("tipo", "r"))
    return [Post(*post) for post in sentence.execute(select_one=False)]

def get_from_user(post: Post) -> list:
    sentence = Sentence(post).select().where(('autor_id', post.autor_id)).where(('tipo', post.tipo))
    return [Post(*post_) for post_ in sentence.execute(select_one=False)]