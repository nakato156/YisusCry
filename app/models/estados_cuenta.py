from app.database.Model import BaseModel
from os import getenv
import attr

@attr.s()
class estados_cuenta(BaseModel):
    id:int
    nombre: str =   attr.field(validator=[attr.validators.instance_of(str), attr.validators.max_len(40)])

    def __attrs_post_init__(self):
        setattr(self, "__table", getenv("BD_TABLE_USERS"))
        self.__table = getenv("BD_TABLE_ESTADOS_CUENTA")
        self.fields = attr.asdict(self).keys()
        super().__init__()

    def get_object(self, ignore:tuple = ()) -> dict:
        if ignore: return {k:v for k,v in attr.asdict(self).items() if not k in ignore}
        return attr.asdict(self)
