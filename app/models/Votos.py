from app.database.bd import BaseModel
from peewee import UUIDField, ForeignKeyField, IntegerField, DateTimeField
from app.models import User
from app.models.Posts import Post
from datetime import datetime

class Voto(BaseModel):
    uuid: str         = UUIDField(primary_key=True, null=False)
    post_id: str    = ForeignKeyField(Post, backref='Votos')
    autor_id: str   = ForeignKeyField(User, backref='Votos')
    votos_up: int   = IntegerField(default=0)
    votos_dn: int   = IntegerField(default=0)
    fecha: datetime      = DateTimeField()

    class Meta:
        table_name = 'Votos'