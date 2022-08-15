from ..models.Contratos import Contrato
from .Model import Sentence

def save(contrato: Contrato) -> Contrato:
    Sentence(contrato).save()
    return contrato

def get_one(contrato: Contrato) -> Contrato:
    sentence = Sentence(contrato).select().where(('user_id', contrato.user_id))
    return sentence.execute()
