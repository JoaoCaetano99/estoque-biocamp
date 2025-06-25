from flask import Blueprint, jsonify, request
from models import db, Produto, Movimentacao
from datetime import datetime
from app import app  # garante que o app e o db já estão inicializados

api_bp = Blueprint('api', __name__, url_prefix='/api')

# 1. Lista produtos
@api_bp.route('/produtos', methods=['GET'])
def list_produtos():
    prods = Produto.query.order_by(Produto.nome).all()
    result = [{
        'id': p.id,
        'nome': p.nome,
        'saldo': p.saldo,
        'minimo': p.minimo
    } for p in prods]
    return jsonify(result), 200

# 2. Lista movimentações
@api_bp.route('/movimentacoes', methods=['GET'])
def list_movimentacoes():
    produto_id = request.args.get('produto_id', type=int)
    query = Movimentacao.query
    if produto_id:
        query = query.filter_by(produto_id=produto_id)
    movs = query.order_by(Movimentacao.datahora.desc()).all()
    result = [{
        'id': m.id,
        'produto_id': m.produto_id,
        'quantidade': m.quantidade,
        'tipo': m.tipo,
        'datahora': m.datahora.isoformat(),
        'saldo_apos': m.saldo_apos
    } for m in movs]
    return jsonify(result), 200

# 3. Histórico (mesma coisa que /movimentacoes, mas sem filtro)
@api_bp.route('/historico', methods=['GET'])
def historico():
    return list_movimentacoes()
