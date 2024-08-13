from mysql_db import get_db_connection

class Categoria:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Categoria")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_by_id(categoria_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Categoria WHERE Id = %s", (categoria_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def add(descripcion):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Categoria (Descripcion) VALUES (%s)", (descripcion,))
        conn.commit()
        conn.close()

    @staticmethod
    def update(categoria_id, descripcion):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Categoria SET Descripcion = %s WHERE Id = %s", (descripcion, categoria_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(categoria_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Categoria WHERE Id = %s", (categoria_id,))
        conn.commit()
        conn.close()
