from app.database.bd import BD

class Log(BD):
    def __init__(self, table_name:str) -> None:
        super().__init__()
        self.table = table_name
    
    def log(self, data:dict)->bool:
        try:
            campos = ",".join(f"`{campo}`" for campo in data.keys())
            values = ",".join(f"'{val}'" for val in data.values())
            self.execute(f"INSERT INTO `{self.table}` ({campos}) VALUES ({values})")
            return True
        except: return False
