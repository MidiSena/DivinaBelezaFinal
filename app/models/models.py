from datetime import datetime
from tkinter import CASCADE
from flask_login import UserMixin
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class Clientes(db.Model):
    cliente_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    sobrenome = db.Column(db.String(64), nullable=False)
    cpf = db.Column(db.BigInteger, unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)  
    telefone = db.Column(db.String(80), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

class Funcionarios(db.Model, UserMixin):
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    sobrenome = db.Column(db.String(64), nullable=False)
    cpf = db.Column(db.BigInteger, unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    telefone = db.Column(db.String(80), nullable=False)
    administrador = db.Column(db.String(3), nullable=False)
    senha = db.Column(db.VARCHAR(164), nullable=False)

@login_manager.user_loader
def user_loader(id):
    return Funcionarios.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    nome = request.form.get('username')
    usuario = Funcionarios.query.filter_by(nome=nome).first()
    return usuario if usuario else None

def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)

class Servicos(db.Model):
    __tablename__ = 'servicos'
    servico_id = db.Column(db.Integer, primary_key=True)
    servico = db.Column(db.String(64), unique=True, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    tempo = db.Column(db.Integer, nullable=False)
    
class Agendamentos(db.Model):
    __tablename__='agendamentos'
    agendamento_id = db.Column(db.Integer, primary_key=True)
    agendamento_data = db.Column(db.DateTime, nullable=False)
    agendamento_data_fim = db.Column(db.DateTime, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.cliente_id', onupdate="cascade", ondelete="cascade"))
    servico_id = db.Column(db.Integer, db.ForeignKey('servicos.servico_id', onupdate="cascade", ondelete="cascade"))
    id = db.Column(db.Integer, db.ForeignKey('funcionarios.id', onupdate="cascade", ondelete="cascade"))
