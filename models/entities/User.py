from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id_sesion, username, password, mail="", phone="", profile_pic="", description="", address="") -> None:
        self.id = id_sesion
        self.username = username
        self.password = password
        self.mail = mail 
        self.profile_pic = profile_pic 
        self.description = description 
        self.phone = phone
        self.address = address 

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    