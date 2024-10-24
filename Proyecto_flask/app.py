from flask import *
from flask_mysqldb import MySQL
from flask_cors import CORS
import random
import string
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)

#folder donde se guardaran las imagenes
UPLOAD_FOLDER = 'assets/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app, resources={r"/*": {"origins": "*"}})

#conexion con la base de datos 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'dbRestaurantes'
mysql = MySQL(app)

app.config['JWT_SECRET_KEY'] = 'seminarioFinal2'
jwt = JWTManager(app)

def upload_file(image_base64, filename):
    
    # Verifica si es una extensión permitida
    try:
        image_data = base64.b64decode(image_base64)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(file_path, 'wb') as image_file:
            image_file.write(image_data)
        return True
    except Exception as e:
        return  False
    
    return False

#validar inicio de sesion 
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    if not username or not password:
        return jsonify({"message": "El usuario y la contraseña son requeridos para iniciar sesión"}), 400

    query = """
        SELECT Usuario.Usuario, Usuario.Password, Usuario.Tipo_User, Clientes.Nombres, Clientes.Apellidos, Clientes.Telefono, Clientes.email 
        FROM dbRestaurantes.Usuario 
        INNER JOIN  dbRestaurantes.Clientes on Usuario.id_user = Clientes.id 
        WHERE Usuario.Usuario = %s 
        Union 
        SELECT Usuario.Usuario, Usuario.Password, Usuario.Tipo_User, Empleados.Nombres, Empleados.Apellidos, Empleados.Telefono, Empleados.email 
        FROM dbRestaurantes.Usuario 
        INNER JOIN  dbRestaurantes.Empleados on Usuario.id_user = Empleados.id 
        WHERE Usuario.Usuario = %s
    """

    cur = mysql.connection.cursor()

    # Ejecuta la consulta
    cur.execute(query, (username, username))

    # Verifica si hay una fila
    result = cur.fetchone()
    if result:
        stored_password_hash = result[1]  # Asumiendo que el hash de la contraseña está en la segunda columna
        
        # Verifica si la contraseña es correcta
        if check_password_hash(stored_password_hash, password):
            token = create_access_token(identity=username)
            # Excluye la contraseña antes de devolver el resultado
            user_data = {
                "Usuario": result[0],
                "Tipo_User": result[2],
                "Nombres": result[3],
                "Apellidos": result[4],
                "Telefono": result[5],
                "email": result[6]
            }
            return jsonify({"data": user_data, "token": token}), 200
        else:
            return jsonify({"message": "Contraseña incorrecta"}), 401
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404
       
#crear una cuenta
@app.route('/crear_cuenta', methods=['POST'])
def crear_cuenta():
    data = request.json
    email = data['email']
    email = email.upper()
    nombres = data['nombres']
    apellidos = data['apellidos']
    telefono = data['telefono']
    password = data['password']
    confirm_password = data['password2']
    if not email or not nombres or not apellidos or not telefono or not password:
        return jsonify({"message": "Todos los campos son requeridos"}), 400
    if password != confirm_password:
        return jsonify({"message": "las contraseñas no son iguales"}), 400
    
    try:
        cur = mysql.connection.cursor()
        # Inserta los datos en la tabla Clientes
        query_clientes = """
        INSERT INTO Clientes (Email, Nombres, Apellidos, Telefono, FechaCreacion, FechaActualizacion)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        now = datetime.now()
        cur.execute(query_clientes, (email, nombres, apellidos, telefono, now, now))
        # Obtener el id del cliente recién creado
        cliente_id = cur.lastrowid
        # Crear hash de la contraseña
        hashed_password = generate_password_hash(password)
        # Inserta el usuario en la tabla Usuario
        query_usuario = """
        INSERT INTO Usuario (Usuario, Password, id_user, Tipo_user)
        VALUES (%s, %s, %s, %s)
        """
        tipo_usuario = 1  # Tipo de usuario fijo (1) para este caso
        cur.execute(query_usuario, (email, hashed_password, cliente_id, tipo_usuario))
        # Confirmar ambas transacciones
        mysql.connection.commit()
        return jsonify({"message": "Cuenta y usuario creados exitosamente"}), 200
    except Exception as e:
        print(f"Error al crear la cuenta: {e}")
        mysql.connection.rollback()  # Revertir transacción en caso de error
        return jsonify({"message": "Error al crear la cuenta"}), 500


#-------por revisar-----------
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

#-------fin por revisar-----------

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

# Retrieve all employees
@app.route('/getEmpleados', methods=['GET'])
def getEmpleados():
    cur = mysql.connection.cursor()
    query = """
        SELECT Empleados.id, Empleados.Email, Empleados.Nombres, Empleados.Apellidos, 
		Empleados.Telefono, Empleados.Id_Puesto, Puestos.Descripcion as Puesto, 
        Empleados.Salario, Usuario.Usuario, Empleados.Imagen
        FROM dbRestaurantes.Empleados 
        INNER JOIN dbRestaurantes.Puestos ON Puestos.Id=Empleados.Id_Puesto
        INNER JOIN dbRestaurantes.Usuario ON Usuario.id_user=Empleados.id
    """
    cur.execute(query)
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

    email = data["email"]
    email = email.upper()
    password = generate_password_hash(email)

    nombreImagen = data["nombres"] + data["apellidos"] + data["usuario"] + "." + data["mimetype"]
    
    if not upload_file(data["image"], nombreImagen):
        return jsonify({'error': "No fue posible guardar la imagen"}), 500


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

@app.route('/menu', methods=['GET'])
def get_menu_items():
    cur = mysql.connection.cursor()
    cur.execute('SELECT Menu.Id, Menu.Titulo, Menu.Descripcion, Menu.Precio, Menu.Id_Categoria, Categoria.descripcion as categoria, promocion FROM dbRestaurantes.Menu INNER JOIN dbRestaurantes.Categoria ON Categoria.Id = Menu.Id_Categoria')
    rows = cur.fetchall()
    cur.close()

    platillos = []
    for row in rows:
        platillo = {
            "Id": row[0],
            "Titulo": row[1],
            "Descripcion": row[2],
            "Precio": row[3],
            "Id_Categoria": row[4],
            "Categoria": row[5],
            "Promo": row[6],
        }
        platillos.append(platillo)

    return jsonify(platillos), 200

@app.route('/menu', methods=['POST'])
def add_menu_item():
    data = request.json
    cursor = mysql.connection.cursor()

    query = """
    INSERT INTO Menu (Titulo, Descripcion, Precio, Id_Categoria, promocion)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        data['Titulo'],
        data['Descripcion'],
        data['Precio'],
        data['Id_Categoria'],
        data['promo']
    )

    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Platillo agregado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/menu/<int:id>', methods=['PUT'])
def update_menu_item(id):
    data = request.json
    cursor = mysql.connection.cursor()

    query = """
    UPDATE Menu 
    SET Titulo = %s, Descripcion = %s, Precio = %s, Id_Categoria = %s, FechaActualizacion = %s 
    WHERE Id = %s
    """
    values = (
        data['Titulo'],
        data['Descripcion'],
        data['Precio'],
        data['Id_Categoria'],
        datetime.now(),
        id
    )

    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Platillo actualizado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/menu/<int:id>', methods=['DELETE'])
def delete_menu_item(id):
    cursor = mysql.connection.cursor()
    query = """
    DELETE FROM Menu WHERE Id = %s
    """
    
    try:
        cursor.execute(query, (id,))
        mysql.connection.commit()
        cursor.close()

        if cursor.rowcount == 0:
            return jsonify({'message': 'No se encontró el platillo'}), 404
        
        return jsonify({'message': 'Platillo eliminado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500




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

    
if __name__ == '__main__':
    app.run(debug=True)