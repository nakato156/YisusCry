from os import getenv
import cryptocode

class Role():
    ROLES = {
        0: "user",
        1: "yisus",
        2: "admin"
    }

    def __init__(self, role: str) -> None:
        self._tk = getenv("TKROLE")
        self.roles = (int(rol) for rol in  self.__decrypt(role).split(";"))
        self.roles = {rol:Role.ROLES.get(rol) for rol in self.roles}

    def has(self, rol) -> bool:
        return rol in self.roles.values()

    def __encrypt(self, roles: list) -> str:
        return cryptocode.encrypt(";".join(roles), self._tk)

    def __decrypt(self, hash_: str) -> str:
        return cryptocode.decrypt(hash_, self._tk)
    
    def add(self, rol: str):
        for k,v in Role.ROLES.items():
            if v == rol: self.roles[k] = v
        else: raise ValueError("Rol inexistente")
    
    def pop(self, rol: str):
        if rol == "user": return
        elif rol in self.roles.values(): self.roles.pop(rol)
        else: raise ValueError("Rol no asignado")

    @classmethod
    def convert(cls, roles: list[int]) -> str:
        roles_ = (str(k) for k,v in Role.ROLES.items() if v in roles)
        return cryptocode.encrypt(";".join(roles_), getenv("TKROLE"))

    def __repr__(self):
        return self.__encrypt([str(k) for k in self.roles.keys()])