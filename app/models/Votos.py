from app.database.Model import BaseModel, Sentence
from attr import s as attrS, field
from os import getenv

@attrS
class Voto(BaseModel):
    id: int
    post_id: str    = field()
    autor_id: str   = field()
    fecha: str      = field(default="")

    def __attrs_post_init__(self):
        setattr(self, "__table", getenv("BD_TABLE_VOTOS"))
        super().__init__()

    def get(self, campos:tuple = ()) -> int:
        sentence = Sentence(self).select()
        if campos:
            for campo in campos:
                sentence = sentence.where((campo, getattr(self, campo)))
        else:
            sentence = sentence.where(("post_id", self.post_id)) \
                .where(("autor_id", self.autor_id))
        res = self.execute(sentence.count())
        print(res)
        return res
