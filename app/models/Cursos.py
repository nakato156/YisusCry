from app.database.Model import BaseModel
from os import getenv
from attr import s as attrS, field, validators

@attrS()
class Curso(BaseModel):
    uuid: str       =   field(default="", validator=[validators.instance_of(str), validators.max_len(37)])
    nombre: str     =   field(default="")
    foto: str       =   field(default="")
    
    def __attrs_post_init__(self):
        setattr(self, "__table", getenv("BD_TABLE_CURSOS"))
        self.__table = getenv("BD_TABLE_CUENTAS_USERS")
        super().__init__()
