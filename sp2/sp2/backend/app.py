from flask import Flask, jsonify, request, send_from_directory, render_template, url_for # Añadir send_from_directory
from google.cloud import vision
from flask_mysqldb import MySQL
from flask_cors import CORS
import os
import cv2
import qrcode
import numpy as np

app = Flask(__name__)
CORS(app)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\jairf\OneDrive\Documentos\GitHub\Seminario2\sp2\sp2\backend\lateral-boulder-439501-f1-014fb3e367c0.json"
vision_client = vision.ImageAnnotatorClient()

# Configuración de la conexión con la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'dbRestaurantes'
mysql = MySQL(app)

def test_db_connection():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")  # Una consulta simple para probar la conexión
        cur.fetchone()
        cur.close()
        return jsonify({'message': 'Conexión a la base de datos exitosa!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/images', methods=['GET'])
def get_images():
    images = [
        {"id": 1, "name": "Imagen 1", "src": "http://localhost:5000/static/imagen1.png"},
        {"id": 2, "name": "Imagen 2", "src": "http://localhost:5000/static/imagen2.png"},
        {"id": 3, "name": "Imagen 3", "src": "http://localhost:5000/static/imagen3.png"},
        {"id": 4, "name": "Imagen 4", "src": "http://localhost:5000/static/imagen4.png"},
        {"id": 5, "name": "Imagen 5", "src": "http://localhost:5000/static/baños.png"}
    ]
    return jsonify(images)

# Ruta para crear una nueva reserva
@app.route('/reservas', methods=['POST'])
def crear_reserva():
    data = request.json  # Obtener los datos del formulario en formato JSON

    # Validar que todos los campos requeridos estén presentes
    required_fields = ['id_usuario', 'id_estado', 'fecha_reserva', 'hora_reserva', 'cantidad_personas', 'mesa']
    if not all(key in data for key in required_fields):
        return jsonify({'error': 'Datos incompletos'}), 400

    # Crear la consulta SQL para insertar la reserva
    query = """
        INSERT INTO formulario_reserva (id_usuario, id_estado, fecha_reserva, hora_reserva, cantidad_personas, comentarios, mesa)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    # Obtener los valores de los datos
    values = (
        data['id_usuario'],
        data['id_estado'],
        data['fecha_reserva'],
        data['hora_reserva'],
        data['cantidad_personas'],
        data.get('comentarios', ''),  # Usar el comentario solo si existe
        data['mesa'],  # Asegúrate de que este campo esté presente
    )

    try:
        # Crear un cursor y ejecutar la consulta
        cur = mysql.connection.cursor()
        cur.execute(query, values)
        mysql.connection.commit()  # Confirmar los cambios
        cur.close()  # Cerrar el cursor

        return jsonify({'message': 'Reserva creada con éxito'}), 201
    except Exception as e:
        # Manejar errores, imprimiendo el error en el log para depuración
        print(f"Error al crear la reserva: {str(e)}")  # Imprimir el error en el log
        return jsonify({'error': str(e)}), 500  # Devolver el error al cliente


@app.route('/get_reservas/<int:id>', methods=['GET'])
def get_reservation(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM formulario_reserva WHERE id_reserva = %s", (id,))
        reservation = cur.fetchone()
        cur.close()

        if reservation:
            return jsonify({
                'id_reserva': reservation[0],
                'id_usuario': reservation[1],
                'id_estado': reservation[2],
                'fecha_reserva': str(reservation[3]),  # Asegúrate de que sea de tipo string
                'hora_reserva': str(reservation[4]),    # Asegúrate de que sea de tipo string
                'cantidad_personas': reservation[5],
                'mesa': reservation[6],
                'comentarios': reservation[7],
                'fecha_creacion': str(reservation[8])   # Asegúrate de que sea de tipo string
            })
        else:
            return jsonify({'error': 'Reserva no encontrada'}), 404
    except Exception as e:
        print(f"Error al obtener la reserva: {str(e)}")  # Imprimir el error en el log
        return jsonify({'error': 'Error interno del servidor'}), 500


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/analyze', methods=['POST'])
def analyze_image():
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
    
if __name__ == '__main__':
    app.run(debug=True)

