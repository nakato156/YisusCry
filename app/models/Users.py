from app.database.Model import BaseModel
from app.functions.RoleManager import Role
from hashlib import sha256
from os import getenv
import attr

def valid(condicion: bool):
    if not condicion: raise ValueError()

@attr.s()
class User(BaseModel):
    uuid: str =     attr.field(default="",  validator=[attr.validators.instance_of(str), attr.validators.max_len(37)])
    email: str =    attr.field(default="",  validator=[attr.validators.instance_of(str), attr.validators.max_len(100)])
    username: str = attr.field(default="",  validator=[attr.validators.instance_of(str), attr.validators.max_len(90)])
    codigo: str =   attr.field(default="",  validator=[attr.validators.instance_of(str), attr.validators.max_len(11)])
    password: str = attr.field(default="",  validator=attr.validators.instance_of(str), repr=False)
    carrera: str =  attr.field(default="",  validator=[attr.validators.instance_of(str), attr.validators.max_len(100)])
    edad: int =     attr.field(default=0,   validator=[attr.validators.instance_of(int),  lambda _, _attr,val:  valid(val in range(90))])
    ciclo: int =    attr.field(default=0,   validator=[attr.validators.instance_of(int),  lambda _, _attr,val: valid(val in range(11))])
    info:str   =    attr.field(default="",  validator=[attr.validators.instance_of(str), attr.validators.max_len(200)], converter=lambda x: str(x) if x else "")
    fecha: str =    attr.field(default="")
    role:str =      attr.field(default='pw==*zaNDWhNkWE6nfKNFzUrOxg==*Lad3Ppi6a3VCpH/6GCyudg==*O3fmPCh+W3WHTJfVqM9Iww==')

    def __attrs_post_init__(self):
        setattr(self, "__table", getenv("BD_TABLE_USERS"))
        self.__table = getenv("BD_TABLE_USERS")
        self.fields = attr.asdict(self).keys()
        super().__init__()

    def get_object(self, ignore:tuple = (), convert: bool = False) -> dict:
        if convert: self.role = Role(self.role)
        if self.password: self.password = sha256(self.password.encode()).hexdigest()
        if ignore: return {k:v for k,v in attr.asdict(self).items() if not k in ignore}
        return attr.asdict(self)
