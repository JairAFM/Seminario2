from mysql_db import get_db_connection

class Restaurantes:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Restaurante")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_by_id(restaurante_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Restaurante WHERE Id = %s", (restaurante_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def add(restaurante):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Restaurante (Direccion, Telefono, FechaCreacion, FechaActualizacion)
            VALUES (%s, %s, NOW(), NOW())
        """, (restaurante['direccion'], restaurante['telefono']))
        conn.commit()
        conn.close()

    @staticmethod
    def update(restaurante_id, restaurante):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Restaurante SET Direccion = %s, Telefono = %s, FechaActualizacion = NOW()
            WHERE Id = %s
        """, (restaurante['direccion'], restaurante['telefono'], restaurante_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(restaurante_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Restaurante WHERE Id = %s", (restaurante_id,))
        conn.commit()
        conn.close()
