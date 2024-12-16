from flask import *
from flask_mysqldb import MySQL
from flask_cors import CORS
import random
import string
from datetime import datetime, timedelta
import os
from google.cloud import vision
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
import base64
import openai

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "..\\lateral-boulder-439501-f1-014fb3e367c0.json"

# Inicializar el cliente de Google Vision
vision_client = vision.ImageAnnotatorClient()

#credenciales de openai
openai.api_key = "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"

#conexion con la base de datos 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'dbRestaurantes'
mysql = MySQL(app)

app.config['JWT_SECRET_KEY'] = 'seminarioFinal2'
jwt = JWTManager(app)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    """
    Sirve las imágenes guardadas en la carpeta uploads.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload_menu/<filename>', methods=['GET'])
def uploaded_menu(filename):
    """
    Sirve las imágenes guardadas en la carpeta uploads.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER']+'menus/', filename)


def upload_file(image_base64, filename, menu = False):
    
    # Verifica si es una extensión permitida
    try:
        image_data = base64.b64decode(image_base64)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if menu:
            file_path = os.path.join(UPLOAD_FOLDER + 'menus/', filename)
        
        with open(file_path, 'wb') as image_file:
            image_file.write(image_data)
        return {'success': True, 'message': ''}
    except Exception as e:
        return {'success': False, 'message': str(e)}

#validar inicio de sesion 
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    if not username or not password:
        return jsonify({"message": "El usuario y la contraseña son requeridos para iniciar sesión"}), 400

    query = """
        SELECT Usuario.Usuario, Usuario.Password, Usuario.id_user, Usuario.Tipo_User, Clientes.Nombres, Clientes.Apellidos, Clientes.Telefono, Clientes.email 
        FROM dbRestaurantes.Usuario 
        INNER JOIN  dbRestaurantes.Clientes on Usuario.id_user = Clientes.id 
        WHERE Usuario.Usuario = %s 
        Union 
        SELECT Usuario.Usuario, Usuario.Password, Usuario.id_user, Usuario.Tipo_User, Empleados.Nombres, Empleados.Apellidos, Empleados.Telefono, Empleados.email 
        FROM dbRestaurantes.Usuario 
        INNER JOIN  dbRestaurantes.Empleados on Usuario.id_user = Empleados.id 
        WHERE Usuario.Usuario = %s
    """

    cur = mysql.connection.cursor()

    cur.execute(query, (username, username))

    result = cur.fetchone()
    if result:
        stored_password_hash = result[1] 
        
        if check_password_hash(stored_password_hash, password):
            token = create_access_token(identity=username)
            user_data = {
                "Usuario": result[0],
                "Id_User": result[2],
                "Tipo_User": result[3],
                "Nombres": result[4],
                "Apellidos": result[5],
                "Telefono": result[6],
                "email": result[7]
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
        query_clientes = """
        INSERT INTO Clientes (Email, Nombres, Apellidos, Telefono, FechaCreacion, FechaActualizacion)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        now = datetime.now()
        cur.execute(query_clientes, (email, nombres, apellidos, telefono, now, now))
        cliente_id = cur.lastrowid
        hashed_password = generate_password_hash(password)
        query_usuario = """
        INSERT INTO Usuario (Usuario, Password, id_user, Tipo_user)
        VALUES (%s, %s, %s, %s)
        """
        tipo_usuario = 1  
        cur.execute(query_usuario, (email, hashed_password, cliente_id, tipo_usuario))
        mysql.connection.commit()
        return jsonify({"message": "Cuenta y usuario creados exitosamente"}), 200
    except Exception as e:
        print(f"Error al crear la cuenta: {e}")
        mysql.connection.rollback()  
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
    INSERT INTO dbrestaurantes.reservaciones (id_mesa, id_cliente, id_orden, inicio, hora, no_personas, id_estado) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) 
    """
    values = (
       data['id_mesa'],data['id_cliente'], data['id_orden'],
        data['inicio'], data['hora'], data['no_personas'], data['id_estado']
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
            'id': reserva[2],
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
            'id': reserva[2],
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
    categories = []
    for row in rows:
        category = {
            "id": row[0],
            "description": row[1]
        }
        categories.append(category)
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
        INNER JOIN dbRestaurantes.Usuario ON Usuario.id_user=Empleados.id and Usuario.Tipo_User = 0
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
            "id_imagen": row[9],
        }
        empleados.append(empleado)
    return jsonify(empleados)

# Insert employee into Empleados table
@app.route('/newEmpleado', methods=['POST'])
def newEmpleado():
    data = request.json

    user_pass = data["usuario"]
    user_pass = user_pass.upper()

    cursor = mysql.connection.cursor()

    query = "Select 1 from dbrestaurantes.usuario where usuario = %s"
    try: 
        cursor.execute(query, (user_pass,))
        result = cursor.fetchone()
        if result:
            return jsonify({'error': "El usuario ya existe"}), 500
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

    password = generate_password_hash(user_pass)

    nombreImagen = data["nombres"] + data["apellidos"] + user_pass + "." + data["mimetype"]
    
    subirImagen = upload_file(data["image"], nombreImagen)
    if not subirImagen["success"]:
        return jsonify({'error': "No fue posible guardar la imagen" + subirImagen["message"]}), 500


    query = """ 
    INSERT INTO Empleados 
    (Email, Nombres, Apellidos, Telefono, Id_Puesto, Salario, imagen, FechaCreacion, FechaActualizacion)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    now = datetime.now()
    values = (
        data['email'],
        data['nombres'],
        data['apellidos'],
        data['telefono'],
        data['puesto'],
        data['salario'],
        nombreImagen,  
        now,
        now
    )

    try:
        cur = mysql.connection.cursor()
        cur.execute(query, values)
        idEmployee = cur.lastrowid
        values_user = (
                user_pass,
                password,
                idEmployee,
                0
            )
        query_usuario = """
        INSERT INTO Usuario (Usuario, Password, id_user, Tipo_user)
        VALUES (%s, %s, %s, %s)
        """
        cur.execute(query_usuario, values_user)
        
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

    nombreImagen = data["nombres"] + data["apellidos"] + data["usuario"] + "." + data["mimetype"]
    
    subirImagen = upload_file(data["image"], nombreImagen)
    if not subirImagen["success"]:
        return jsonify({'error': "No fue posible guardar la imagen" + subirImagen["message"]}), 500
    
    query = """ 
    UPDATE dbRestaurantes.Empleados 
    SET Email = %s, Nombres = %s, Apellidos = %s, Telefono = %s, Id_Puesto = %s, Salario = %s, imagen = %s, FechaActualizacion = %s 
    WHERE Id = %s
    """
    values = (
        data['email'],
        data['nombres'],
        data['apellidos'],
        data['telefono'],
        data['id_puesto'],
        data['salario'],
        nombreImagen,
        datetime.now(),
        id
    )
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Empleado actualizado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

# Delete an employee by ID
@app.route('/deleteEmpleado/<int:id>/<string:usuario>', methods=['DELETE'])
def deleteEmpleado(id, usuario):
    cursor = mysql.connection.cursor()
    query = """ 
    DELETE FROM dbRestaurantes.Empleados 
    WHERE Id = %s
    """
    query_user = """ 
    DELETE FROM dbRestaurantes.Usuario 
    WHERE usuario = %s
    """
    try:
        cursor.execute(query_user, (usuario,))
        cursor.execute(query, (id,))
        mysql.connection.commit()
        cursor.close()

        if cursor.rowcount == 0:
            return jsonify({'message': 'No se encontró el empleado'}), 404
        
        return jsonify({'message': 'Empleado eliminado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

#obtiene ids de las mesas existentes
@app.route('/checkMesa', methods=['GET'])
def check_mesa():
    cursor = mysql.connection.cursor()

    try:
        query = "SELECT DISTINCT id FROM dbRestaurantes.Mesas"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        ids = [row[0] for row in result]

        return jsonify({'ids': ids}), 200

    except Exception as e:
        print("Error al obtener IDs de las mesas:", str(e)) 
        cursor.close()
        return jsonify({'error': str(e)}), 500

#agregar nueva mesa
@app.route('/newMesa', methods=['POST'])
def newMesa():
    data = request.json
    cursor = mysql.connection.cursor()
    query = """

    INSERT INTO Mesas (id, capacidad, posicion_x, posicion_y, imagenes, num_mesa)
    VALUES (%s, %s, %s, %s, CAST(%s AS JSON), %s)
    """
    values = (
        data['id'],
        data['capacidad'],
        data['posicion_x'],
        data['posicion_y'],
        data['imagenes'],
        data['num_mesa'],
    )
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Mesa creada exitosamente'}), 200
    except Exception as e:
        print("Error al crear mesa:", str(e))  
        cursor.close()
        return jsonify({'error': str(e)}), 500

#actualizar mesa
@app.route('/editMesa/<int:id>', methods=['PUT'])
def editMesa(id):
    data = request.json
    cursor = mysql.connection.cursor()
    query = """
    UPDATE dbRestaurantes.mesas
    SET capacidad = %s,
        posicion_x = %s,
        posicion_y = %s,
        imagenes = %s
    WHERE id = %s
    """
    values = (
        data['capacidad'],
        data['posicion_x'],
        data['posicion_y'],
        data['imagenes'], 
        id
    )
    try:
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Mesa actualizada exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/menu', methods=['GET'])
def get_menu_items():
    cur = mysql.connection.cursor()
    cur.execute('SELECT Menu.Id, Menu.Titulo, Menu.Descripcion, Menu.Precio, Menu.Id_Categoria, Categoria.descripcion as categoria, promocion, precio_promo, fechaIni_promo, fechaFin_promo, imagenes FROM dbRestaurantes.Menu INNER JOIN dbRestaurantes.Categoria ON Categoria.Id = Menu.Id_Categoria')
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
            "Precio_Promo": row[7],
            "FechaIni_Promo": row[8],
            "FechaFin_Promo": row[9],
            "Imagenes": row[10],
        }
        platillos.append(platillo)

    return jsonify(platillos), 200

@app.route('/menu', methods=['POST'])
def add_menu_item():
    data = request.json

    imagenes = json.loads(data["image"])
    imagenesGuardadas = []

    for img in imagenes:
        subirImagen = upload_file(img["image"], img["name"], True)
        if not subirImagen["success"]:
            return jsonify({'error': "No fue posible guardar la imagen" + subirImagen["message"]}), 500
        else:
            imagenesGuardadas.append(img["name"])

    insert_query = """
    INSERT INTO Menu 
        (Titulo, Descripcion, Precio, Id_Categoria, promocion, precio_promo, fechaIni_promo, fechaFin_promo, imagenes, FechaCreacion, FechaActualizacion) 
    VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    now = datetime.now()

    values = (
        data['Titulo'],
        data['Descripcion'],
        data['Precio'],
        data['Id_Categoria'],
        data['promo'],
        data['precio_promo'],
        data['inicio_promo'],
        data['fin_promo'],
        json.dumps(imagenesGuardadas),
        now,
        now
    )

    try:
        cursor = mysql.connection.cursor()
        cursor.execute(insert_query, values)
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Platillo agregado exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/menu/<int:id>', methods=['PUT'])
def update_menu_item(id):
    data = request.json

    imagenes = json.loads(data["image"])
    imagenesGuardadas = []

    for img in imagenes:
        subirImagen = upload_file(img["image"], img["name"], True)
        if not subirImagen["success"]:
            return jsonify({'error': "No fue posible guardar la imagen" + subirImagen["message"]}), 500
        else:
            imagenesGuardadas.append(img["name"])
    now = datetime.now()
    query = """
    UPDATE Menu 
        SET Titulo = %s,
            Descripcion = %s,
            Precio = %s,
            Id_categoria = %s,
            promocion = %s,
            precio_promo = %s,
            fechaIni_promo = %s,
            fechaFin_promo = %s,
            imagenes = %s,
            FechaActualizacion = %s
        WHERE Id = %s
    """
    values = (
        data['Titulo'],
        data['Descripcion'],
        data['Precio'],
        data['Id_Categoria'],
        data['promo'],
        data['precio_promo'],
        data['inicio_promo'],
        data['fin_promo'],
        data['image'],
        now,
        id,
    )

    if 'Id_Categoria' in data:
        query = """
        UPDATE Menu 
            SET Titulo = %s,
                Descripcion = %s,
                Precio = %s,
                Id_Categoria = %s,
                promocion = %s,
                precio_promo = %s,
                fechaIni_promo = %s,
                fechaFin_promo = %s,
                FechaActualizacion = %s
            WHERE Id = %s
        """
        values = (
            data['Titulo'],
            data['Descripcion'],
            data['Precio'],
            data['Id_Categoria'],
            data['promo'],
            data['precio_promo'],
            data['inicio_promo'],
            data['fin_promo'],
            now,
            id,
        )

    if imagenesGuardadas:
        query = """
        UPDATE Menu 
            SET Titulo = %s,
                Descripcion = %s,
                Precio = %s,
                Id_Categoria = %s,
                promocion = %s,
                precio_promo = %s,
                fechaIni_promo = %s,
                fechaFin_promo = %s,
                imagenes = %s,
                FechaActualizacion = %s
            WHERE Id = %s
        """
        values = (
            data['Titulo'],
            data['Descripcion'],
            data['Precio'],
            data['Id_Categoria'],
            data['promo'],
            data['precio_promo'],
            data['inicio_promo'],
            data['fin_promo'],
            json.dumps(imagenesGuardadas),
            now,
            id,
        )

    try:
        cursor = mysql.connection.cursor()
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

@app.route('/getPromos', methods=['GET'])
def getPromos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT Menu.Id, Menu.Titulo, Menu.Descripcion, Menu.Precio, Menu.Id_Categoria, Categoria.descripcion as categoria, promocion, precio_promo, fechaIni_promo, fechaFin_promo, imagenes FROM dbRestaurantes.Menu INNER JOIN dbRestaurantes.Categoria ON Categoria.Id = Menu.Id_Categoria where promocion = 1 and sysdate() <= fechaFin_promo')
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
            "Precio_Promo": row[7],
            "FechaIni_Promo": row[8],
            "FechaFin_Promo": row[9],
            "Imagenes": row[10],
        }
        platillos.append(platillo)

    return jsonify(platillos), 200

@app.route('/getPlatillosCat/<int:id>', methods=['GET'])
def getPlatillosCat(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT Menu.Id, Menu.Titulo, Menu.Descripcion, Menu.Precio, Menu.Id_Categoria, Categoria.descripcion as categoria, promocion, precio_promo, fechaIni_promo,fechaFin_promo, imagenes FROM dbRestaurantes.Menu INNER JOIN dbRestaurantes.Categoria ON Categoria.Id = Menu.Id_Categoria where Categoria.Id = %s', (id,))
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
            "Precio_Promo": row[7],
            "FechaIni_Promo": row[8],
            "FechaFin_Promo": row[9],
            "Imagenes": row[10],
        }
        platillos.append(platillo)
    return jsonify(platillos), 200



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


#mesas
@app.route('/getMesas', methods=['GET'])
def get_mesas():
    try:
        cursor = mysql.connection.cursor()
        
        query = """
        SELECT * 
        FROM dbRestaurantes.mesas
        """
        
        cursor.execute(query)
        mesas = cursor.fetchall()  
        cursor.close()
        
        if mesas:
            mesas_list = []
            for mesa in mesas:
                mesas_list.append({
                    'id': mesa[0],
                    'capacidad': mesa[1],
                    'imagenes': mesa[2],
                    'posicion_x': mesa[3],
                    'posicion_y': mesa[4],
                    'num_mesa': mesa[5]
                })
            return jsonify(mesas_list), 200
        else:
            return jsonify({
                'message': 'No se encontraron mesas'
            }), 404
            
    except Exception as e:
        print(f"Error al obtener las mesas: {str(e)}")
        if cursor:
            cursor.close()
        return jsonify({
            'error': 'Error al obtener las mesas',
            'details': str(e)
        }), 500


@app.route('/verReservas/<int:id>', methods=['GET'])
def ver_reservas(id):
    cursor = mysql.connection.cursor()
    
    try:
        query = """
        SELECT a.id_mesa, a.id_orden, a.inicio, hora, a.no_personas, b.descripcion
        FROM dbrestaurantes.reservaciones a, dbrestaurantes.estadosreserva b 
        WHERE a.Id_Cliente = %s
        """
        cursor.execute(query, (id,))
        result = cursor.fetchall()
        cursor.close()

        if not result:
            return jsonify({'message': 'No se encontraron reservas para este cliente.'}), 404

        reservas = []
        for row in result:
            reservas.append({
                'id_mesa': row[0],  
                'id_orden': row[1],      
                'inicio': row[2],      
                'hora': row[3].total_seconds() if isinstance(row[3], timedelta) else row[3],     
                'no_personas': row[4],
                'descripcion': row[5],          
            })

        return jsonify(reservas), 200
    except Exception as e:
        print("Error al obtener reservas:", str(e))  
        cursor.close()
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No se ha proporcionado ninguna imagen.'}), 400

    file = request.files['image']
    content = file.read()

    image = vision.Image(content=content)
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations

    labels_list = [label.description for label in labels]

    if labels_list:
        description = f"Este platillo está compuesto por: {', '.join(labels_list[:-1])}, y {labels_list[-1]}."
    else:
        description = "No se pudieron identificar ingredientes para este platillo."

    return jsonify({'description': description})

@app.route('/generar_desc', methods=['POST'])
def generar_desc():
    data = request.json
    prompt = data.get('prompt', '')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150
        )
        return jsonify(response.choices[0].message['content'].strip())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deleteMesa/<int:id>', methods=['DELETE'])
def delete_mesa(id):
    try:
        cursor = mysql.connection.cursor()

        query = "DELETE FROM dbRestaurantes.mesas WHERE id = %s"
        
        cursor.execute(query, (id,))
        mysql.connection.commit()  
        
        if cursor.rowcount > 0:
            cursor.close()
            return jsonify({
                'message': f'Mesa con id {id} eliminada exitosamente.'
            }), 200
        else:
            cursor.close()
            return jsonify({
                'message': f'No se encontró una mesa con id {id}.'
            }), 404

    except Exception as e:
        print(f"Error al eliminar la mesa {id}: {str(e)}")
        if cursor:
            cursor.close()
        return jsonify({
            'error': 'Error al eliminar la mesa',
            'details': str(e)
        }), 500

@app.route('/getConfiguracion', methods=['GET'])
def getConfiguracion():
    try:
        cursor = mysql.connection.cursor()
        
        query = """
        SELECT id, color, descripcion
        FROM Configuraciones 
        WHERE id = %s
        """
        
        cursor.execute(query, (1,))
        config = cursor.fetchone()
        cursor.close()
        
        if config:
            return jsonify({
                'id': config[0],
                'color': config[1],
                'descripcion': config[2]
            }), 200
        else:
            return jsonify({
                'message': 'configuracion no encontrada no encontrada',
                'id': 1
            }), 404
            
    except Exception as e:
        print(f"Error al obtener la configuracion: {str(e)}")
        if cursor:
            cursor.close()
        return jsonify({
            'error': 'Error al obtener la configuracion',
            'details': str(e)
        }), 500


@app.route('/configTr', methods=['POST'])
def configTr():
    data = request.json

    # Validación de campos
    if 'opcion' not in data or 'color' not in data or 'descripcion' not in data:
        return jsonify({'error': 'Faltan parámetros en la solicitud'}), 400

    cursor = mysql.connection.cursor()
    try:
        if data["opcion"] == 1:
            query = """
            INSERT INTO Configuraciones (color, descripcion)
            VALUES (%s, %s)
            """
            values = (data['color'], data['descripcion'])
            cursor.execute(query, values)
        else:
            if 'id' not in data:
                return jsonify({'error': 'El campo id es obligatorio para actualizar'}), 400
            query = """ 
            UPDATE Configuraciones 
            SET color = %s, descripcion = %s
            WHERE id = %s 
            """
            values = (data['color'], data['descripcion'], data['id'])
            cursor.execute(query, values)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Configuración procesada exitosamente'}), 200
    except Exception as e:
        cursor.close()
        print("Error al procesar la configuración:", str(e))
        return jsonify({'error': 'Error en el servidor', 'details': str(e)}), 500

@app.route('/obtenerMesa/<int:id>', methods=['GET'])
def get_mesa(id):
    try:
        cursor = mysql.connection.cursor()
        
        # Consulta para obtener la mesa por el id recibido
        query = """
        SELECT capacidad, imagenes, posicion_x, posicion_y, num_mesa
        FROM dbRestaurantes.mesas
        WHERE id = %s
        """
        
        cursor.execute(query, (id,))
        mesa = cursor.fetchone()  # Obtenemos una sola fila (mesa)
        cursor.close()
        
        if mesa:
            mesa_dict = {
                'id': id,
                'capacidad': mesa[0],
                'imagenes': mesa[1],
                'posicion_x': mesa[2],
                'posicion_y': mesa[3],
                'num_mesa': mesa[4]
            }
            return jsonify(mesa_dict), 200
        else:
            return jsonify({
                'message': 'Mesa no encontrada'
            }), 404
    except Exception as e:
        return jsonify({
            'message': f'Error al obtener la mesa: {str(e)}'
        }), 500

@app.route('/actualizar_capacidad/<int:id>', methods=['PUT'])
def actualizar_capacidad(id):
    data = request.json  
    cursor = mysql.connection.cursor()
    
    query = """
    UPDATE dbRestaurantes.mesas
    SET capacidad = %s
    WHERE id = %s
    """
    values = (data['capacidad'], id)
    
    try:
        cursor.execute(query, values)  
        mysql.connection.commit()  
        cursor.close()
        return jsonify({'message': f'Mesa con id {id} actualizada exitosamente'}), 200
    except Exception as e:
        cursor.close()
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
