from ..models import Post, Voto, User, Comment
from typing import List, Tuple
from peewee import fn, JOIN

def crear(post: Post) -> Post:
    post.save()
    return post

def eliminar(post: Post) -> bool:
    try:
        post.delete().where(Post.uuid == post.uuid)
        return True
    except: return False

def actualizar(post: Post) -> Post:
    post.update(post.get_object()).where(Post.uuid == post.uuid)
    return post

def get(limit: int) -> List[Post]:
    return (Post
            .select(Post, Voto, fn.SUM(Voto.votos_up - Voto.votos_dn).alias('votos'))
            .join(Voto, JOIN.LEFT_OUTER, on=(Post.uuid == Voto.post_id))
            .group_by(Post)
            .order_by(Post.fecha_publicado.desc())
            .paginate(1, limit))

def get_recent(limit: int) -> List[Post]:
    query = (Post
            .select(Post, Voto)
            .join(Voto, on=(Post.uuid == Voto.post_id))
            .order_by(Post.fecha_edicion) 
            .paginate(1, limit))
    
    return (res for res in query.execute())

def get_one(post: Post) -> Post:
    return post.get(Post.uuid == post.uuid)

def get_all(tipo: str = "") -> list:
    if tipo: sentence = Post().select().where(Post.tipo == tipo)
    else: sentence = Post().select()
    return [post for post in sentence.execute()]

def get_form_ques(post: Post) -> list:
    return list(Post.select().where(Post.referencia == post.uuid, Post.tipo == "r"))

def get_from_user(user: User, post: Post) -> list:
    posts = Post.select().where(Post.autor_id == user.uuid , Post.tipo == post.tipo)
    return list(posts) if posts else []

def get_post_with_comments(post_id:str) -> Tuple[Post, Comment]:
    post = Post.get(Post.uuid == post_id)
    comments = post.comments

    return post, comments