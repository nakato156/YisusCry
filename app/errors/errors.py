class UserNotFound(Exception):
    def __init__(self, msg: str = "Usuario no encontrado") -> None:
        super().__init__(msg)

class CursoNotFound(Exception):
    def __init__(self, msg: str = "Curso no encontrado") -> None:
        super().__init__(msg)