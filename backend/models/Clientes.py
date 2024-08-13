from mysql_db import get_db_connection

class Cliente:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clientes")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_by_id(cliente_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clientes WHERE Id = %s", (cliente_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def add(cliente):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Clientes (Email, Nombres, Apellidos, Telefono, Password, FechaCreacion, FechaActualizacion)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        """, (cliente['email'], cliente['nombres'], cliente['apellidos'], cliente['telefono'], cliente['password']))
        conn.commit()
        conn.close()

    @staticmethod
    def update(cliente_id, cliente):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Clientes SET Email = %s, Nombres = %s, Apellidos = %s, Telefono = %s, Password = %s, FechaActualizacion = NOW()
            WHERE Id = %s
        """, (cliente['email'], cliente['nombres'], cliente['apellidos'], cliente['telefono'], cliente['password'], cliente_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(cliente_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Clientes WHERE Id = %s", (cliente_id,))
        conn.commit()
        conn.close()
