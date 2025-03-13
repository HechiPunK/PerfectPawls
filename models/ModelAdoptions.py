from .entities.Adoptions import Adoption
from .entities.User import User

#agregue idsesion
class ModelAdoptions:
    @classmethod
    def get_all(self, db):
        try:
            cursor = db.connection.cursor()
            sql = """
            SELECT id_adoption, image, name, type, sex, age, size, color, sterilized, vaccinated, description, id_sesion 
            FROM adoptions
            """
            cursor.execute(sql)
            results = cursor.fetchall()

            adoptions = []
            for row in results:
                adoption = Adoption(
                    id=row[0],
                    image=row[1],
                    name=row[2],
                    type=row[3],
                    sex=row[4],
                    age=row[5],
                    size=row[6],
                    color=row[7],
                    sterilized=row[8],
                    vaccinated=row[9],
                    description=row[10],
                    id_sesion=row[11]
                )
                adoptions.append(adoption)
            return adoptions
        except Exception as ex:
            raise Exception(ex)
         
    @classmethod
    def add_adoption(self, db, adoption):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO adoptions (image, name, type, sex, age, size, color, sterilized, vaccinated, description, id_sesion)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (adoption.image, adoption.name, adoption.type, adoption.sex, adoption.age, adoption.size, adoption.color, adoption.sterilized, adoption.vaccinated, adoption.description, adoption.id_sesion))
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

#Esta madre es nueva para sacar las adopciones por usuario que las sube
    @classmethod
    def get_by_id(cls, db, id_sesion):
        try:
            cursor = db.connection.cursor()
            # Asegúrate de que uses el placeholder adecuado para evitar inyecciones SQL
            sql = """
            SELECT id_adoption, image, name, type, sex, age, size, color, sterilized, vaccinated, description FROM adoptions WHERE id_sesion = %s
            """
            cursor.execute(sql, (id_sesion,))  # Pasando la tupla con el parámetro
            results = cursor.fetchall()

            adoptions = []
            for row in results:
                adoption = Adoption(
                    id=row[0],
                    image=row[1],
                    name=row[2],
                    type=row[3],
                    sex=row[4],
                    age=row[5],
                    size=row[6],
                    color=row[7],
                    sterilized=row[8],
                    vaccinated=row[9],
                    description=row[10],   
                    id_sesion=id_sesion               
                )

                adoptions.append(adoption)
            return adoptions
        except Exception as ex:
            raise Exception(f"Error en la consulta: {ex}")


    @classmethod
    def delete(cls, db, id, id_sesion):
        try:
            cursor = db.connection.cursor()
            # Verificar si la adopción existe y si el usuario logueado es el dueño
            sql_check = "SELECT id_sesion FROM adoptions WHERE id_adoption = %s"
            cursor.execute(sql_check, (id,))
            result = cursor.fetchone()

            if result and result[0] == id_sesion:  # Verifica si el usuario logueado es el dueño
                sql = "DELETE FROM adoptions WHERE id_adoption = %s"
                cursor.execute(sql, (id,))
                db.connection.commit()
                return True
            else:
                return False  # No se puede eliminar si no es el dueño
        except Exception as ex:
            raise Exception(f"Error al eliminar la adopción: {ex}")

    @classmethod
    def get_adoption_by_id(cls, db, id_adoption):
        try:
            cursor = db.connection.cursor()
            sql = """
            SELECT id_adoption, image, name, type, sex, age, size, color, sterilized, vaccinated, description, id_sesion
            FROM adoptions WHERE id_adoption = %s
            """
            cursor.execute(sql, (id_adoption,))
            row = cursor.fetchone()
            if row:
                return Adoption(
                    id=row[0],
                    image=row[1],
                    name=row[2],
                    type=row[3],
                    sex=row[4],
                    age=row[5],
                    size=row[6],
                    color=row[7],
                    sterilized=row[8],
                    vaccinated=row[9],
                    description=row[10],
                    id_sesion=row[11]
                )
            return None
        except Exception as ex:
            raise Exception(f"Error en la consulta: {ex}")