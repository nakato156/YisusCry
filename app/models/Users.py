from app.database.bd import BaseModel
from peewee import UUIDField, CharField, IntegerField, DateTimeField, TextField
from app.functions.RoleManager import Role
from hashlib import sha256
from playhouse.shortcuts import model_to_dict


class YisusUsers(BaseModel):
    uuid: str =     UUIDField(primary_key=True, null=False)
    email: str =    CharField(max_length=100)
    username: str = CharField(max_length=90)
    codigo: str =   CharField(max_length=11)
    password: str = CharField()
    id_estado_cuenta: int = IntegerField(default=1)
    carrera: str =  CharField(max_length=100)
    edad: int =     IntegerField(null=False)
    ciclo: int =    IntegerField(default=1, null=False)
    info:str   =    CharField(max_length=200)
    fecha_creacion: str =    DateTimeField()
    role:str =      TextField(default='pw==*zaNDWhNkWE6nfKNFzUrOxg==*Lad3Ppi6a3VCpH/6GCyudg==*O3fmPCh+W3WHTJfVqM9Iww==')
    hash_foto:str = TextField(default="")

    def get_object(self, exclude:tuple = (), convert: bool = False) -> dict:
        if convert: self.role = Role(self.role)
        if self.password: self.password = sha256(self.password.encode()).hexdigest()
        if exclude: return {k:v for k,v in model_to_dict(self, exclude=exclude)}
        return model_to_dict(self)

    class Meta:
        table_name = 'YisusUsers'