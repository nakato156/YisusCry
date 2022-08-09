from app.database.Model import BaseModel
from os import getenv
from attr import s as attrS, field, validators, asdict

@attrS()
class Comment(BaseModel):
    uuid: str       =   field(default="", validator=[validators.instance_of(str), validators.max_len(37)])
    comentario: str =   field(default="", validator=[validators.instance_of(str), validators.max_len(200)])
    user_id:str     =   field(default="", validator=[validators.instance_of(str), validators.max_len(37)])
    post_id:str     =   field(default="", validator=[validators.instance_of(str), validators.max_len(37)])
    fecha: str      =   field(default="")
    username: str   =   field(default="")

    def __attrs_post_init__(self):
        setattr(self, "__table", getenv("BD_TABLE_COMMENTS"))
        self.__table = getenv("BD_TABLE_COMMENTS")
        self.fields = asdict(self).keys()
        super().__init__()