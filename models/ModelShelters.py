from .entities.Shelter import Shelter

class ModelShelters:

    @classmethod
    def login(self, db, shelter):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_shelter, name, password FROM shelters 
                     WHERE name = '{}'""".format(shelter.name)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row is not None:
                # Verificar la contraseña
                valid_password = Shelter.check_password(row[2], shelter.password)
                return Shelter(row[0], row[1], valid_password) if valid_password else None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_shelter, name, email, address, manager, description, img FROM shelters WHERE id_shelter = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()

            if row is not None:
                return Shelter(
                    id=row[0],
                    name=row[1],
                    password=None,  # No recuperar contraseña aquí
                    email=row[2],
                    address=row[3],
                    manager=row[4],
                    description=row[5],
                    img=row[6]
                )
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register(self, db, shelter):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id_shelter FROM shelters WHERE name = %s OR email = %s"
            cursor.execute(sql, (shelter.name, shelter.email))
            if cursor.fetchone() is not None:
                return False
            
            # Hashear la contraseña
            hashed_password = Shelter.hash_password(shelter.password)
            sql = """INSERT INTO shelters (name, email, password, address, manager, description, img) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (
                shelter.name, shelter.email, hashed_password, 
                shelter.address, shelter.manager, shelter.description, shelter.img
            ))
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)