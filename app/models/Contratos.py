from app.database.bd import BaseModel
from peewee import UUIDField, ForeignKeyField, DoubleField, DateField
from datetime import datetime
from .Users import YisusUsers as User
from os import getenv

table_name_ = getenv("BD_TABLE_CUENTAS_USERS")

class Contrato(BaseModel):
    uuid: str       =   UUIDField(null=False)
    user_id: str    =   ForeignKeyField(User, backref=table_name_)
    client_id: str  =   ForeignKeyField(User, backref=table_name_)
    monto: float    =   DoubleField(null=False)
    fecha: datetime =   DateField()


    class Meta:
        table_name = table_name_