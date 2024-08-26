from flask import *
from flask_mysqldb import MySQL


app = Flask(__name__)

#rutas de pantallas
@app.route('/')
def inicio():
    return render_template('views/index.html')

@app.route('/login')
def login():
    return render_template('views/iniciosesion.html')

@app.route('/crear')
def crear():
    return render_template('views/crear_cuenta.html')

#conexion con la base de datos 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'restaurantes'
mysql = MySQL(app)

#validar inicio de sesion 
@app.route('/inicio_sesion', methods=['GET'])
def inicio_sesion():
    if request.method == 'GET':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM proyecto.clientes WHERE EMAIL = ' + email + 'AND PASSWORD =' + password)
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
        cur.execute('INSERT INTO proyecto.clientes (email, nombre, apellido, telefono, password, fecha_creacion) VALUES (%s, %s, %s, %s, %s, NOW())', 
                    (email, nombre, apellido, telefono, password))
        mysql.connection.commit()
        return 'received'

#ver las mesas disponibles
@app.route('/reservar', methods=['GET'])
def mesas():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM proyecto.mesas')
        mysql.connection.commit()
        return 'received'
    
if __name__ == '__main__':
    app.run(debug= True)
