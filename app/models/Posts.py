from app.database.Model import BaseModel, Sentence
from attr import s as attrS, field, validators, asdict
from os import getenv

@attrS
class Post(BaseModel):
    uuid:str            =   field(default="")
    autor_id:str        =   field(default="", validator=[validators.instance_of(str), validators.max_len(55)])
    titulo:str          =   field(default="", validator=[validators.instance_of(str), validators.max_len(55)])
    contenido:str       =   field(default="", validator=[validators.instance_of(str)])
    votos_up: int       =   field(default=0)
    votos_dn: int       =   field(default=0)
    fecha_publicado:str =   field(default="", repr=False)
    fecha_edicion:str   =   field(default="", repr=False)
    tipo:str            =   field(default="")
    referencia: str     =   field(default="")

    def __attrs_post_init__(self):
        setattr(self, "__table", getenv("BD_TABLE_POSTS"))
        self.__table = getenv("BD_TABLE_POSTS")
        self.fields = asdict(self).keys()
        super().__init__()

    def get_object(self, ignore: tuple = (), detail: bool = False):
        data = {k:v for k,v in asdict(self).items() if not k in ignore}
        if not detail:
            data["votos"] = data["votos_up"] - data["votos_dn"]
            data.pop("votos_up")
            data.pop("votos_dn")
        return data

    def data_pago(self) -> dict:
        return {
            "transaction_amount": 5.5,
            "description": "Publicación de pregunta"
        }