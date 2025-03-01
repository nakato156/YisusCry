from app.database.bd import BaseModel
from peewee import UUIDField, CharField

class Estados_cuenta(BaseModel):
    id:int      = UUIDField(primary_key=True, null=False)
    nombre: str =   CharField(max_length=40)