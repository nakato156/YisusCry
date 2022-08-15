from app.database.Model import BaseModel
from os import getenv
from attr import s as attrS, field

@attrS()
class Contrato():
    uuid: str       =   field(default="")
    user_id: str    =   field(default="")
    client_id: str  =   field(default="")
    monto: float    =   field(default=.0)
    id: int         =   field(default=0)
    fecha: str      =   field(default="")

    def __attrs_post_init__(self):
        setattr(self, "__table", getenv("BD_TABLE_CUENTAS_USERS"))
        self.__table = getenv("BD_TABLE_CUENTAS_USERS")
        super().__init__()
