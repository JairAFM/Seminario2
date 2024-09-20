from flask import *
from flask_mysqldb import MySQL
from flask_cors import CORS
import random
import string
from datetime import datetime



app = Flask(__name__)
CORS(app) 

#rutas de pantallas
@app.route('/')
def inicio():
    return render_template('views/index.html')

#pantalla de inicio de sesion
@app.route('/login')
def login():
    return render_template('views/login.html')

#pantalla de crear cuenta
@app.route('/crear')
def crear():
    return render_template('views/crear_cuenta.html')

#pantalla de reservar mesa
@app.route('/reserva')
def reserva():
    return render_template('views/reserva.html')

#conexion con la base de datos 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'dbRestaurantes'
mysql = MySQL(app)

#validar inicio de sesion 
@app.route('/inicio_sesion', methods=['GET'])
def inicio_sesion():
    if request.method == 'GET':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM dbRestaurantes.clientes WHERE EMAIL = ' + email + 'AND PASSWORD =' + password)
        mysql.connection.commit()
        return 'received'
    
#crear una cuenta
@app.route('/crear_cuenta', methods=['POST'])
def crear_cuenta():
    if request.method == 'POST':
        email = request.form['email']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        password = request.form['password']
        confirm_password = request.form['password2']

        if password != confirm_password:
            return 'las contraseñas no son iguales'
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO dbRestaurantes.clientes (email, nombre, apellido, telefono, password, fecha_creacion) VALUES (%s, %s, %s, %s, %s, NOW())', 
                    (email, nombre, apellido, telefono, password))
        mysql.connection.commit()
        return 'received'

#ver las mesas disponibles
@app.route('/reservar', methods=['GET'])
def mesas():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM dbRestaurantes.mesas')
        mysql.connection.commit()
        return 'received'

@app.route('/reservaciones', methods=['POST'])
def crear_reserva():
    data = request.json
    cursor = mysql.connection.cursor()
    query = """ 
    INSERT INTO reservaciones (id_usuario, id_mesa, id_restaurante, fecha, hora, id_estado, observaciones) 
    VALUES (%s, %s, %s, %s, %s, %s, %s) 
    """
    values = (
        data['id_usuario'], data['id_mesa'], data['id_restaurante'],
        data['fecha'], data['hora'], data['id_estado'], data['observaciones']
    )
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Reserva creada exitosamente'}), 201
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/eliminar_reserva/<int:id>', methods=['DELETE'])
def cancelar_reserva(id):
    cursor = mysql.connection.cursor()
    query = """
    UPDATE reservaciones 
    SET id_estado = (SELECT id_estado FROM estados WHERE nombre = 'cancelada') 
    WHERE id = %s
    """
    try:
        cursor.execute(query, (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Reserva cancelada exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/obtener_reserva/<int:id>', methods=['GET'])
def obtener_reserva(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM reservaciones WHERE id = %s"
    cursor.execute(query, (id,))
    reserva = cursor.fetchone()
    cursor.close()
    if reserva:
        return jsonify({
            'id': reserva[0],
            'id_usuario': reserva[1],
            'id_mesa': reserva[2],
            'id_restaurante': reserva[3],
            'fecha': reserva[4],
            'hora': reserva[5],
            'id_estado': reserva[6],
            'observaciones': reserva[7]
        }), 200
    else:
        return jsonify({'error': 'Reserva no encontrada'}), 404

@app.route('/reserva_usuario/<int:id_usuario>', methods=['GET'])
def obtener_reservas_usuario(id_usuario):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM reservaciones WHERE id_usuario = %s"
    cursor.execute(query, (id_usuario,))
    reservas = cursor.fetchall()
    cursor.close()
    return jsonify([
        {
            'id': reserva[0],
            'id_usuario': reserva[1],
            'id_mesa': reserva[2],
            'id_restaurante': reserva[3],
            'fecha': reserva[4],
            'hora': reserva[5],
            'id_estado': reserva[6],
            'observaciones': reserva[7]
        } for reserva in reservas
    ]), 200

@app.route('/actualizar_reserva/<int:id>', methods=['PUT'])
def actualizar_reserva(id):
    data = request.json
    cursor = mysql.connection.cursor()
    query = """ 
    UPDATE reservaciones 
    SET fecha = %s, hora = %s, observaciones = %s 
    WHERE id = %s 
    """
    values = (data['fecha'], data['hora'], data['observaciones'], id)
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Reserva actualizada exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

#ver las categorias disponibles
@app.route('/getCategories', methods=['GET'])
def getCategories():
    cur = mysql.connection.cursor()
    cur.execute('SELECT ID, DESCRIPCION FROM dbRestaurantes.Categoria')
    rows = cur.fetchall()
    cur.close()
    # Convert the result into a list of dictionaries
    categories = []
    for row in rows:
        category = {
            "id": row[0],
            "description": row[1]
        }
        categories.append(category)
    # Return the results as a JSON response
    return jsonify(categories)

#insert categorias disponibles
@app.route('/newCategoria', methods=['POST'])
def newCategoria():
    data = request.json
    cursor = mysql.connection.cursor()
    query = """ 
    INSERT INTO dbRestaurantes.Categoria(Descripcion)
    VALUES (%s) 
    """
    values = (
        data['description'],
    )
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Categoria creada exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

#update categorias disponibles
@app.route('/editCategoria/<int:id>', methods=['PUT'])
def editCategoria(id):
    data = request.json
    cursor = mysql.connection.cursor()
    query = """ 
    UPDATE dbRestaurantes.Categoria 
    SET Descripcion = %s 
    WHERE Id = %s
    """
    values = (
        data['description'],
        id
    )
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Categoria actualizada exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

# Delete category by ID
@app.route('/deleteCategoria/<int:id>', methods=['DELETE'])
def deleteCategoria(id):
    cursor = mysql.connection.cursor()
    query = """ 
    DELETE FROM dbRestaurantes.Categoria 
    WHERE Id = %s
    """
    try:
        cursor.execute(query, (id,))
        mysql.connection.commit()
        cursor.close()

        if cursor.rowcount == 0:
            return jsonify({'message': 'No se encontró la categoría'}), 404
        
        return jsonify({'message': 'Categoria eliminada exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

# Get all puestos
@app.route('/getPuestos', methods=['GET'])
def getPuestos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT Id, Descripcion FROM dbRestaurantes.Puestos')
    rows = cur.fetchall()
    cur.close()
    puestos = []
    for row in rows:
        puesto = {
            "id": row[0],
            "description": row[1]
        }
        puestos.append(puesto)
    return jsonify(puestos)

# Insert new puesto
@app.route('/newPuesto', methods=['POST'])
def newPuesto():
    data = request.json
    cursor = mysql.connection.cursor()
    query = "INSERT INTO dbRestaurantes.Puestos (Descripcion) VALUES (%s)"
    values = (data['description'],)
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Puesto creado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

# Update puesto by ID
@app.route('/editPuesto/<int:id>', methods=['PUT'])
def editPuesto(id):
    data = request.json
    cursor = mysql.connection.cursor()
    query = "UPDATE dbRestaurantes.Puestos SET Descripcion = %s WHERE Id = %s"
    values = (data['description'], id)
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Puesto actualizado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

# Delete puesto by ID
@app.route('/deletePuesto/<int:id>', methods=['DELETE'])
def deletePuesto(id):
    cursor = mysql.connection.cursor()
    query = "DELETE FROM dbRestaurantes.Puestos WHERE Id = %s"
    try:
        cursor.execute(query, (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Puesto eliminado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

# Utility function to generate an 8-character password based on the employee's name
def generate_password(name):
    # Create a simple password from the first four characters of the name and four random characters
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    password = (name[:4] + random_chars).ljust(8, '0')  # Ensure the password is exactly 8 characters
    return password

# Save image to Imagenes table
def save_image(nombre, imagen, tipo):
    cursor = mysql.connection.cursor()
    query = """ 
    INSERT INTO dbRestaurantes.Imagenes (Nombre, Tipo, Imagen) 
    VALUES (%s, %s, %s)
    """
    values = (nombre, tipo, imagen)
    try:
        cursor.execute(query, values)
        image_id = cursor.lastrowid  # Get the last inserted image ID
        mysql.connection.commit()
        cursor.close()
        return image_id
    except Exception as e:
        cursor.close()
        return None

# Retrieve all employees
@app.route('/getEmpleados', methods=['GET'])
def getEmpleados():
    cur = mysql.connection.cursor()
    cur.execute('SELECT Empleados.id, Empleados.Email, Empleados.Nombres, Empleados.Apellidos, Empleados.Telefono, Empleados.Id_Puesto, Puestos.Descripcion as Puesto, Empleados.Salario, Empleados.Usuario, Imagenes.Imagen, Empleados.Id_Imagen FROM dbRestaurantes.Empleados INNER JOIN dbRestaurantes.Puestos ON Puestos.Id=Empleados.Id_Puesto INNER JOIN dbRestaurantes.Imagenes ON Imagenes.Id=Empleados.Id_Imagen')
    rows = cur.fetchall()
    cur.close()
    empleados = []
    for row in rows:
        empleado = {
            "id": row[0],
            "email": row[1],
            "nombres": row[2], 
            "apellidos": row[3],
            "telefono": row[4],
            "id_puesto": row[5],
            "puesto": row[6],
            "salario": row[7],
            "usuario": row[8],
            "id_imagen": row[10],
        }
        empleados.append(empleado)
    return jsonify(empleados)

# Insert employee into Empleados table
@app.route('/newEmpleado', methods=['POST'])
def newEmpleado():
    data = request.json
    password = generate_password(data['nombres'] + data["apellidos"])

    nombreImagen = data["nombres"] + data["apellidos"] + data["email"]
    tipoImagen = 0
    id_imagen = save_image(nombreImagen, data["image"], tipoImagen)
    if id_imagen is None :
        return jsonify({'error': "No ha sido posible guardar la imagen"}), 500
    # Generate password from the employee's name

    cursor = mysql.connection.cursor()

    query = """ 
    INSERT INTO Empleados 
    (Email, Nombres, Apellidos, Telefono, Id_Puesto, Salario, Usuario, Password, Id_Imagen, FechaCreacion, FechaActualizacion)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['email'],
        data['nombres'],
        data['apellidos'],
        data['telefono'],
        data['puesto'],
        data['salario'],
        data['usuario'],
        password,  # Use the generated password
        id_imagen,  # Image ID from the previous image save
        datetime.now(),
        datetime.now()
    )

    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Empleado creado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

# Update an employee
@app.route('/editEmpleado/<int:id>', methods=['PUT'])
def editEmpleado(id):
    data = request.json
    cursor = mysql.connection.cursor()

    query = """ 
    UPDATE dbRestaurantes.Empleados 
    SET Email = %s, Nombres = %s, Apellidos = %s, Telefono = %s, Id_Puesto = %s, Salario = %s, Usuario = %s, Password = %s, Id_Imagen = %s, FechaActualizacion = %s 
    WHERE Id = %s
    """
    values = (
        data['email'],
        data['nombres'],
        data['apellidos'],
        data.get('telefono', None),
        data.get('id_puesto', None),
        data['salario'],
        data['usuario'],
        data['password'],
        data.get('id_imagen', None),
        datetime.now(),
        id
    )
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Empleado actualizado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

# Delete an employee by ID
@app.route('/deleteEmpleado/<int:id>', methods=['DELETE'])
def deleteEmpleado(id):
    cursor = mysql.connection.cursor()
    query = """ 
    DELETE FROM dbRestaurantes.Empleados 
    WHERE Id = %s
    """
    try:
        cursor.execute(query, (id,))
        mysql.connection.commit()
        cursor.close()

        if cursor.rowcount == 0:
            return jsonify({'message': 'No se encontró el empleado'}), 404
        
        return jsonify({'message': 'Empleado eliminado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/getMesas', methods=['GET'])
def getMesas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT Id, Capacidad FROM dbRestaurantes.Mesas')
    rows = cur.fetchall()
    cur.close()
    mesas = []
    for row in rows:
        mesa = {
            "id": row[0],
            "capacidad": row[1]
        }
        mesas.append(mesa)
    return jsonify(mesas)

@app.route('/newMesa', methods=['POST'])
def newMesa():
    data = request.json
    cursor = mysql.connection.cursor()
    query = "INSERT INTO dbRestaurantes.Mesas (Capacidad) VALUES (%s)"
    values = (data['capacidad'],)
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Mesa creada exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/editMesa/<int:id>', methods=['PUT'])
def editMesa(id):
    data = request.json
    cursor = mysql.connection.cursor()
    query = "UPDATE dbRestaurantes.Mesas SET Capacidad = %s WHERE Id = %s"
    values = (data['capacidad'], id)
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Mesa actualizada exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/deleteMesa/<int:id>', methods=['DELETE'])
def deleteMesa(id):
    cursor = mysql.connection.cursor()
    query = "DELETE FROM dbRestaurantes.Mesas WHERE Id = %s"
    try:
        cursor.execute(query, (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Mesa eliminada exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500



# Obtener todos los platillos
@app.route('/menu', methods=['GET'])
def get_menu():
    try:
        menu_items = Menu.query.all()
        result = [{
            'Id': item.Id,
            'Titulo': item.Titulo,
            'Descripcion': item.Descripcion,
            'Precio': str(item.Precio),
            'Id_Categoria': item.Id_Categoria
        } for item in menu_items]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'message': 'Error al obtener los platillos', 'error': str(e)}), 500

# Crear un nuevo platillo
@app.route('/newMenu', methods=['POST'])
def add_menu():
    try:
        data = request.json
        new_item = Menu(
            Titulo=data['Titulo'],
            Descripcion=data['Descripcion'],
            Precio=data['Precio'],
            Id_Categoria=data['Id_Categoria']
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Platillo agregado exitosamente'}), 201
    except Exception as e:
        return jsonify({'message': 'Error al agregar el platillo', 'error': str(e)}), 500

# Obtener un platillo por ID
@app.route('/menu/<int:id>', methods=['GET'])
def get_menu_item(id):
    try:
        menu_item = Menu.query.get(id)
        if not menu_item:
            return jsonify({'message': 'Platillo no encontrado'}), 404
        return jsonify({
            'Id': menu_item.Id,
            'Titulo': menu_item.Titulo,
            'Descripcion': menu_item.Descripcion,
            'Precio': str(menu_item.Precio),
            'Id_Categoria': menu_item.Id_Categoria
        }), 200
    except Exception as e:
        return jsonify({'message': 'Error al obtener el platillo', 'error': str(e)}), 500

# Actualizar un platillo
@app.route('/menu/<int:id>', methods=['PUT'])
def update_menu_item(id):
    try:
        data = request.json
        menu_item = Menu.query.get(id)
        if not menu_item:
            return jsonify({'message': 'Platillo no encontrado'}), 404

        menu_item.Titulo = data.get('Titulo', menu_item.Titulo)
        menu_item.Descripcion = data.get('Descripcion', menu_item.Descripcion)
        menu_item.Precio = data.get('Precio', menu_item.Precio)
        menu_item.Id_Categoria = data.get('Id_Categoria', menu_item.Id_Categoria)

        db.session.commit()
        return jsonify({'message': 'Platillo actualizado exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': 'Error al actualizar el platillo', 'error': str(e)}), 500

# Eliminar un platillo
@app.route('/menu/<int:id>', methods=['DELETE'])
def delete_menu_item(id):
    try:
        menu_item = Menu.query.get(id)
        if not menu_item:
            return jsonify({'message': 'Platillo no encontrado'}), 404

        db.session.delete(menu_item)
        db.session.commit()
        return jsonify({'message': 'Platillo eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': 'Error al eliminar el platillo', 'error': str(e)}), 500


    
if __name__ == '__main__':
    app.run(debug=True)
