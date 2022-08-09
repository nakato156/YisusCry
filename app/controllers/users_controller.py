from ..models.Users import User
from hashlib import sha256
from ..database import user_bd

def crear(user: User) -> User:
    user.password = sha256(user.password.encode()).hexdigest()
    user = user_bd.crear(user)
    return user

def eliminar(user: User) -> bool:
    return user_bd.eliminar(user)

def actualizar(user: User) -> User:
    user_bd.actualizar(user)
    return user

def auth(user: User) -> User:
    user.password = sha256(user.password.encode()).hexdigest()
    return user_bd.auth(user)

def get_one(user: User) -> User:
    return user_bd.get_one(user)

def get_all() -> list[User]:
    return user_bd.get_all()

def get_data(user: User) -> User:
    return user_bd.get_data(user)

def count_posts(user: User) -> dict:
    return user_bd.count_posts(user)