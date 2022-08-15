from ..models.Contratos import Contrato
from ..database import contratos_db

def save(contrato: Contrato) -> Contrato:
    contratos_db.save(contrato)
    return contrato
