from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Shelter(UserMixin):
    def __init__(self, id, name, password, email="", address="", manager="", description="", img=None) -> None:
        self.id = id
        self.name = name
        self.password = password
        self.email = email
        self.address = address
        self.manager = manager
        self.description = description
        self.img = img  # Imagen asociada al refugio (opcional)

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    