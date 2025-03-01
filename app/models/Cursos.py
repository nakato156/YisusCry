from app.database.bd import BaseModel
from peewee import UUIDField, CharField

class Curso(BaseModel):
    uuid: str       =   UUIDField(primary_key=True, null=False)
    nombre: str     =   CharField()
    foto: str       =   CharField()