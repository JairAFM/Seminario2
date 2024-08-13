from mysql_db import get_db_connection

class Menu:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Menu")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_by_id(menu_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Menu WHERE Id = %s", (menu_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def add(menu):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Menu (Titulo, Descripcion, Precio, Id_Categoria)
            VALUES (%s, %s, %s, %s)
        """, (menu['titulo'], menu['descripcion'], menu['precio'], menu['id_categoria']))
        conn.commit()
        conn.close()

    @staticmethod
    def update(menu_id, menu):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Menu SET Titulo = %s, Descripcion = %s, Precio = %s, Id_Categoria = %s
            WHERE Id = %s
        """, (menu['titulo'], menu['descripcion'], menu['precio'], menu['id_categoria'], menu_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(menu_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Menu WHERE Id = %s", (menu_id,))
        conn.commit()
        conn.close()
