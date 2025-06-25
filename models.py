from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Instância do SQLAlchemy, usada em app.py
db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    senha_hash = db.Column(db.String, nullable=False)
    tipo = db.Column(db.String, nullable=False)  # 'admin' ou 'usuario'

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    saldo = db.Column(db.Integer, default=0, nullable=False)
    minimo = db.Column(db.Integer, default=1, nullable=False)

class Movimentacao(db.Model):
    __tablename__ = 'movimentacoes'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String, nullable=False)  # 'entrada' ou 'saida'
    datahora = db.Column(db.DateTime, nullable=False)
    saldo_apos = db.Column(db.Integer, nullable=False)

    produto = db.relationship('Produto')
    usuario = db.relationship('Usuario')
