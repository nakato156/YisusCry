from app.database.bd import BaseModel
from peewee import UUIDField, ForeignKeyField, CharField, TextField, DateTimeField
from .Users import YisusUsers as User
from datetime import datetime
from os import getenv

class Post(BaseModel):
    uuid:str            =   UUIDField(primary_key=True, null=False)
    autor_id:str        =   ForeignKeyField(User, backref='Posts')
    titulo:str          =   CharField(max_length=55)
    contenido:str       =   TextField()
    fecha_publicado:datetime =   DateTimeField()
    fecha_edicion:datetime   =   DateTimeField()
    tipo:str            =   CharField(max_length=1)
    referencia: str     =   UUIDField(null=True)

    def data_pago(self) -> dict:
        return {
            "transaction_amount": 5.5,
            "description": "Publicación de pregunta"
        }
    class Meta:
        table_name = getenv("BD_TABLE_POSTS")