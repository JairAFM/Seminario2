from mysql_db import get_db_connection

class Puesto:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Puestos")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_by_id(puesto_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Puestos WHERE Id = %s", (puesto_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def add(descripcion):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Puestos (Descripcion) VALUES (%s)", (descripcion,))
        conn.commit()
        conn.close()

    @staticmethod
    def update(puesto_id, descripcion):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Puestos SET Descripcion = %s WHERE Id = %s", (descripcion, puesto_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(puesto_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Puestos WHERE Id = %s", (puesto_id,))
        conn.commit()
        conn.close()
