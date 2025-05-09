from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Inicializar la app
app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Jimenez112233-@localhost/taller_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Inicializar Marshmallow
ma = Marshmallow(app)

# Crear la clase User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

# Crear el esquema de Marshmallow
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

# Crear un usuario
@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']

    new_user = User(name, email)
    db.session.add(new_user)
    db.session.commit()

    user_schema = UserSchema()
    return user_schema.jsonify(new_user)

# Obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return user_schema.jsonify(users)

# Obtener un usuario por id
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    user_schema = UserSchema()
    return user_schema.jsonify(user)

# Actualizar un usuario
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    user.name = request.json['name']
    user.email = request.json['email']
    db.session.commit()

    user_schema = UserSchema()
    return user_schema.jsonify(user)

# Eliminar un usuario
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'Usuario eliminado'}), 200

# Ruta principal para mostrar el HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
