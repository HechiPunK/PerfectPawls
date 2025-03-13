from .entities.Socioeconomic import Socioeconomic

class ModelSocioeconomic:
         
    @classmethod
    def answers(self, db, socioeconomic):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO socioeconomic (pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6, id_sesion)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (socioeconomic.pregunta1, socioeconomic.pregunta2, socioeconomic.pregunta3, socioeconomic.pregunta4, socioeconomic.pregunta5, socioeconomic.pregunta6, socioeconomic.id_sesion))
            db.connection.commit()
            return True
        except Exception as ex:
            db.connection.rollback()
            raise Exception(ex)

    @classmethod
    def get_by_id(cls, db, id_sesion):
        try:
            cursor = db.connection.cursor()
            sql = """
            SELECT id_socioeconomic, pregunta1, pregunta2, pregunta3, pregunta4, pregunta5, pregunta6 
            FROM socioeconomic 
            WHERE id_sesion = %s
            """
            cursor.execute(sql, (id_sesion,))
            row = cursor.fetchone()  # Cambiar fetchall por fetchone para un solo resultado

            if row:
                return Socioeconomic(
                    id=row[0],
                    pregunta1=row[1],
                    pregunta2=row[2],
                    pregunta3=row[3],
                    pregunta4=row[4],
                    pregunta5=row[5],
                    pregunta6=row[6],
                    id_sesion=id_sesion
                )
            return None
        except Exception as ex:
            raise Exception(f"Error en la consulta: {ex}")

