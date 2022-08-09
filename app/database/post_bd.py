from ..models.Posts import Post
from .Model import Sentence

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

def get_one(post: Post) -> Post:
    sentence = Sentence(post).select().where(("uuid", post.uuid))
    return Post(*sentence.execute())

def get_all(tipo: str = "") -> list[Post]:
    sentence = Sentence(Post()).select()
    if tipo: sentence = sentence.where(("tipo", tipo))
    return [Post(*post) for post in sentence.execute(select_one=False)]

def get_form_ques(post: Post) -> list[Post]:
    sentence = Sentence(post).select().where(('referencia', post.uuid)).where(("tipo", "r"))
    return [Post(*post) for post in sentence.execute(select_one=False)]

def get_from_user(post: Post) -> list[Post]:
    sentence = Sentence(post).select().where(('autor_id', post.autor_id)).where(('tipo', post.tipo))
    return [Post(*post_) for post_ in sentence.execute(select_one=False)]