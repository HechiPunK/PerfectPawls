from .entities.User import User

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_sesion, username, password FROM users 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password))
                return user 
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_sesion, username, mail, phone, profile_pic, description, address FROM users WHERE id_sesion = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                return User(row[0], row[1], None, row[2], row[3], row[4], row[5], row[6])  
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def register(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_sesion FROM users WHERE username = %s OR mail = %s"
            cursor.execute(sql, (user.username, user.mail))
            if cursor.fetchone() != None:
                return False 
            #Aqui añadi el phone en el insert
            hashed_password = User.hash_password(user.password)
            sql = """INSERT INTO users (username, mail, password, phone) VALUES (%s, %s, %s, %s)"""
            print(f"Ejecutando consulta: {sql} con los valores {user.username}, {user.mail}, {hashed_password}, {user.phone}")
            cursor.execute(sql, (user.username, user.mail, hashed_password, user.phone))
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)
           
    @classmethod
    def update_profile(cls, db, user):    
        try:
            cursor = db.connection.cursor()
            sql = """
                UPDATE users 
                SET profile_pic = %s, description = %s, phone = %s, address = %s 
                WHERE id_sesion = %s
            """
            params = (user.profile_pic, user.description, user.phone, user.address, user.id)
            print(f"Ejecutando SQL: {sql} con parámetros {params}")  # Debug
            cursor.execute(sql, params)
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            print(f"Error en update_profile: {str(ex)}")  # Debug
            raise Exception(ex)
    