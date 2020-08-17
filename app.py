from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:38828943.docum@localhost/tsreclamos'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class mensaje(db.Model):
    __tablename__ = 'Mensajes'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    tel = db.Column(db.Integer(), unique=True)
    mensaje = db.Column(db.Text())

    def __init__(self, nombre, email, tel, mensaje):
        self.nombre = nombre
        self.email = email
        self.tel = tel
        self.mensaje = mensaje


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        tel = request.form['tel']
        msj = request.form['msj']
        # print(nombre, email, tel, msj)
        if db.session.query(mensaje).filter(mensaje.tel == tel).count() == 0:
            data = mensaje(nombre, email, tel, msj)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('error.html')
        


if __name__ == "__main__":
    app.run( debug = True, port = 8000 )
