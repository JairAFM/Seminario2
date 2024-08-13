from mysql_db import get_db_connection

class Empleado:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Empleados")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_by_id(empleado_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Empleados WHERE Id = %s", (empleado_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def add(empleado):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Empleados (Email, Nombres, Apellidos, Telefono, Id_Puesto, Salario, Usuario, Password, Id_Imagen, FechaCreacion, FechaActualizacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """, (empleado['email'], empleado['nombres'], empleado['apellidos'], empleado['telefono'], empleado['id_puesto'], empleado['salario'], empleado['usuario'], empleado['password'], empleado['id_imagen']))
        conn.commit()
        conn.close()

    @staticmethod
    def update(empleado_id, empleado):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Empleados SET Email = %s, Nombres = %s, Apellidos = %s, Telefono = %s, Id_Puesto = %s, Salario = %s, Usuario = %s, Password = %s, Id_Imagen = %s, FechaActualizacion = NOW()
            WHERE Id = %s
        """, (empleado['email'], empleado['nombres'], empleado['apellidos'], empleado['telefono'], empleado['id_puesto'], empleado['salario'], empleado['usuario'], empleado['password'], empleado['id_imagen'], empleado_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(empleado_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Empleados WHERE Id = %s", (empleado_id,))
        conn.commit()
        conn.close()
