from ..models.Contratos import Contrato

def save(contrato: Contrato) -> Contrato:
    contrato.save()
    return contrato

def get_one(contrato: Contrato) -> Contrato:
    return contrato.get_or_none(Contrato.user_id == contrato.user_id)