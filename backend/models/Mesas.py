from mysql_db import get_db_connection

class Mesas:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Mesas")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_by_id(mesa_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Mesas WHERE Id = %s", (mesa_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def add(mesa):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Mesas (Id_Mesa, Capacidad)
            VALUES (%s, %s)
        """, (mesa['id_mesa'], mesa['capacidad']))
        conn.commit()
        conn.close()

    @staticmethod
    def update(mesa_id, mesa):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Mesas SET Id_Mesa = %s, Capacidad = %s
            WHERE Id = %s
        """, (mesa['id_mesa'], mesa['capacidad'], mesa_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(mesa_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Mesas WHERE Id = %s", (mesa_id,))
        conn.commit()
        conn.close()
