from app.database.bd import BaseModel
from peewee import DateTimeField, ForeignKeyField, TextField, UUIDField
from .Posts import Post, User
from os import getenv

class Comment(BaseModel):    
    uuid: str       =   UUIDField(primary_key=True)
    comentario: str =   TextField(null=False)
    user_id:str     =   ForeignKeyField(User, backref='comments')
    post_id:str     =   ForeignKeyField(Post, backref='comments')
    fecha: str      =   DateTimeField()

    class Meta:
        table_name = getenv("BD_TABLE_COMMENTS")