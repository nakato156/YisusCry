from ..models.Cursos import Curso
from .Model import Sentence
from ..errors import CursoNotFound

def crear(curso: Curso) -> Curso:
    Sentence(curso).save()
    return curso

def eliminar(curso: Curso) -> bool:
    try:
        Sentence(curso).delete().where(('uuid', curso.uuid)).execute()
        return True
    except Exception as e:
        print(e)
        return False

def get(curso: Curso) -> Curso:
    data = Sentence(curso).select()
    campos = curso.get_object(("nombre", "foto"))
    for k,v in campos.items():
        if v: data.where((k, v))
    res = data.execute()
    if not res: raise CursoNotFound()
    return Curso(*res)

def get_all() -> list:
    return [Curso(*curso) for curso in Sentence(Curso()).select().execute(select_one=False)]