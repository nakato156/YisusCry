from app.database.bd import BD
from attr import asdict
from app.functions.decorators import save_logger

class Sentence(BD):
    def __init__(self, modelo):
        super().__init__()
        self.__model        = modelo
        self.tipo           = ""
        self.table: str     = getattr(modelo, "__table")
        self.campos: list   = list(asdict(modelo).keys())
        self.sentence: str  = ""
        self._where: list   = list()
        self._set: list     = list()
        self.func: str      = ""

    def where(self, condicion: tuple, tipo: str = "AND"):
        op = "="
        if len(condicion) == 2: campo, val = condicion
        elif len(condicion) == 3: campo, op, val = condicion
        else: raise ValueError()
        if not tipo.lower() in ["and", "or"]: raise ValueError("tipo no conocido")

        val = self.parse_val(str(val))
        if self._where: condicion = f"{tipo} `{campo}` {op} {val}"
        else: condicion = f"`{campo}` {op} {val}"
        self._where.append(condicion)
        return self

    def match(self):
        for cond in {k:v for k,v in asdict(self.__model).items() if v}.items():
            self.where(cond)
        return self

    def make(self) -> str:
        add = f"{self.func}({self.campos})" if self.func else f"{self.campos}"
        if self.sentence == "SELECT": add += f" FROM {self.table}"
        elif self.sentence == "UPDATE": add = f"{self.table} SET"
        sentence = f"{self.sentence} {add}" + \
                   (','.join(self._set) if self._set else "") + \
                   (' WHERE ' + ' '.join(self._where) if self._where else "")
        return sentence

    def count(self):
        self.func = "count"
        return self

    def free(self, cmd: str, values: tuple = (), results: bool = False):
        cmd = cmd.replace("&TABLE&", getattr(self.__model, "__table"))
        cmd = cmd.format(*(self.parse_val(val) for val in values))
        if results: return self.__select__(cmd, one = False)
        return self.__execute__(cmd)

    def select(self, campos: str = "*"):
        self.sentence = f"SELECT"
        self.tipo = self.sentence
        self.campos = campos
        return self

    def update(self, data: dict):
        self.sentence = "UPDATE"
        self._set = [f"`{campo}` = {self.parse_val(str(val))}" for campo,val in data.items()]
        return self

    def delete(self):
        self.sentence = "DELETE"
        self.campos = ""
        return self

    @save_logger
    def save(self) -> bool:
        """"Al llamar a esta funcion ya na es necesario llamar a execute()"""
        table = getattr(self.__model, "__table")
        data:dict = {k:v for k,v in asdict(self.__model).items() if v}
        campos = self.parse_campos(data.keys())
        values = ','.join(self.parse_val(f"{val}") for val in data.values())
        return not self.__execute__(f"INSERT INTO `{table}` ({campos}) VALUES ({values})")

    @save_logger
    def execute(self, select_one=True):
        if self.tipo == "SELECT": return self.__select__(self.make(), one=select_one)
        else: return self.__execute__(self.make())

    def __repr__(self):
        return self.make()

class BaseModel(BD):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_object(self, ignore:tuple = ()) -> dict:
        return {k: v for k, v in asdict(self).items() if not k in ignore}