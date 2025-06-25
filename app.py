from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

# Carrega variáveis do .env
from dotenv import load_dotenv
load_dotenv()

from models import db, Usuario, Produto, Movimentacao
from auth import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_super_secreta'  # Troque para algo seguro!

# Usa a URL do banco definida no .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# (DICA DE DEBUG) Mostra a URL usada — pode remover depois
print("DATABASE_URL lida:", os.environ.get('DATABASE_URL'))

# Inicializa SQLAlchemy
db.init_app(app)

# Configura Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Registra blueprint de auth
app.register_blueprint(auth_bp)
from api import api_bp
app.register_blueprint(api_bp)

# Carrega usuário a partir do ID salvo na sessão
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rota inicial: lista de produtos
@app.route('/')
@login_required
def estoque():
    produtos = Produto.query.order_by(Produto.nome).all()
    return render_template('estoque.html', produtos=produtos, usuario=current_user)

# Rota para registrar movimentação
@app.route('/movimentacao', methods=['GET', 'POST'])
@login_required
def movimentacao():
    produtos = Produto.query.order_by(Produto.nome).all()
    if request.method == 'POST':
        produto_id = int(request.form['produto_id'])
        quantidade = int(request.form['quantidade'])
        tipo = request.form['tipo']
        produto = Produto.query.get(produto_id)

        # Atualiza saldo
        if tipo == 'entrada':
            produto.saldo += quantidade
        elif tipo == 'saida':
            if produto.saldo < quantidade:
                flash('Saldo insuficiente', 'warning')
                return redirect(url_for('movimentacao'))
            produto.saldo -= quantidade

        # Cria registro de movimentação
        mov = Movimentacao(
            produto_id=produto.id,
            usuario_id=current_user.id,
            quantidade=quantidade if tipo == 'entrada' else -quantidade,
            tipo=tipo,
            datahora=datetime.utcnow(),
            saldo_apos=produto.saldo
        )
        db.session.add(mov)
        db.session.commit()

        flash('Movimentação registrada com sucesso', 'success')
        return redirect(url_for('estoque'))

    return render_template('movimentacao.html', produtos=produtos)

# Rota para histórico de movimentações
@app.route('/historico')
@login_required
def historico():
    movs = Movimentacao.query.join(Usuario).order_by(Movimentacao.datahora.desc()).all()
    return render_template('historico.html', movs=movs)

# Rotas de administração (apenas para admins)
def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.tipo != 'admin':
            flash('Acesso negado: apenas admins', 'danger')
            return redirect(url_for('estoque'))
        return fn(*args, **kwargs)
    return wrapper

# Criação de novos usuários (admin)
@app.route('/admin/usuarios', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_usuarios():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        tipo = request.form['tipo']
        hash_senha = generate_password_hash(senha)
        novo = Usuario(nome=nome, email=email, senha_hash=hash_senha, tipo=tipo)
        db.session.add(novo)
        db.session.commit()
        flash('Usuário criado!', 'success')
        return redirect(url_for('admin_usuarios'))
    users = Usuario.query.all()
    return render_template('admin_usuarios.html', users=users)

# Criação de novos produtos (admin)
@app.route('/admin/produtos', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_produtos():
    if request.method == 'POST':
        nome = request.form['nome']
        minimo = int(request.form['minimo'])
        novo = Produto(nome=nome, saldo=0, minimo=minimo)
        db.session.add(novo)
        db.session.commit()
        flash('Produto criado!', 'success')
        return redirect(url_for('admin_produtos'))
    prods = Produto.query.all()
    return render_template('admin_produtos.html', produtos=prods)

if __name__ == '__main__':
    # Para desenvolvimento, debug=True
    app.run(debug=True)
