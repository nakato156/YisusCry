import mysql.connector
from typing import Any
from os import getenv
import re
from peewee import MySQLDatabase, Model
from playhouse.shortcuts import model_to_dict

# Configuración de la base de datos
config = {
    "host": getenv("BD_HOST"),
    "database": getenv("BD_NAME"),
    "user": getenv("BD_USER"),
    "password": getenv("BD_PASS"),
}
mysql_db = MySQLDatabase(**config)

# Clase base del modelo
class BaseModel(Model):
    class Meta:
        database = mysql_db
    
    def get_object(self, recurse=True, backrefs=False, only=None,
                exclude=None, seen=None, extra_attrs=None,
                fields_from_query=None, max_depth=None, manytomany=False)-> dict:
        return model_to_dict(self, recurse=recurse, backrefs=backrefs, only=only,
                    exclude=exclude, seen=seen, extra_attrs=extra_attrs,
                    fields_from_query=fields_from_query, max_depth=max_depth, manytomany=manytomany)
    
class BD:
    def __init__(self, **kwargs):
        config = {
            "host": getenv("BD_HOST"),
            "database": getenv("BD_NAME"),
            "username": getenv("BD_USER"),
            "password": getenv("BD_PASS"),
            "port": int(getenv("BD_PORT"))
        }
        self.mysql = mysql.connector
        self.config = config if not kwargs else kwargs
        
    def parse_campos(self, campos:list):
        return ','.join(f"`{campo}`" for campo in campos)
    
    def parse_val(self, val:str):
        return val if val.isdigit() else f"'{re.escape(val)}'"

    def quit(self, conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()

    def __execute__(self, cmd:str):
        conn = self.mysql.connect(**self.config)
        cursor = conn.cursor()
        cursor.execute(cmd)
        self.quit(conn, cursor)
    
    def __select__(self, cmd:str, one=True):
        conn = self.mysql.connect(**self.config)
        cursor = conn.cursor()
        cursor.execute(cmd)
        data = cursor.fetchone() if one else cursor.fetchall()
        self.quit(conn, cursor)
        return data
