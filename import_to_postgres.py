import json
from models import db, Produto, Movimentacao
from app import app

# 1. Importa PRODUTOS
with open('produtos_firestore.json', encoding='utf-8') as f:
    produtos = json.load(f)

produto_nome_para_id = {}

with app.app_context():
    for item in produtos:
        # Só importa os campos válidos
        if not Produto.query.filter_by(nome=item['nome']).first():
            prod = Produto(
                nome=item['nome'],
                saldo=item['saldo'],
                minimo=item['minimo']
            )
            db.session.add(prod)
            db.session.flush()  # Garante acesso ao ID após inserir
            produto_nome_para_id[item['nome']] = prod.id
        else:
            # Se já existe, pega o ID existente
            prod = Produto.query.filter_by(nome=item['nome']).first()
            produto_nome_para_id[item['nome']] = prod.id
    db.session.commit()
    print(f"Importados {len(produtos)} produtos.")

# 2. Importa MOVIMENTAÇÕES (associa pelo nome do produto)
with open('movimentacoes_firestore.json', encoding='utf-8') as f:
    movs = json.load(f)

importados = 0
with app.app_context():
    for item in movs:
        # Descobre nome do produto pelo produtoId no JSON de movimentações
        produto_id_firestore = item['produtoId']
        # Procura pelo nome correspondente no arquivo de produtos
        nome_produto = None
        for p in produtos:
            if p['id'] == produto_id_firestore:
                nome_produto = p['nome']
                break
        if not nome_produto:
            continue  # pula movimentações sem correspondência de produto
        produto = Produto.query.filter_by(nome=nome_produto).first()
        if not produto:
            continue
        mov = Movimentacao(
            produto_id=produto.id,
            usuario_id=None,
            quantidade=item['quantidade'],
            tipo=item['tipo'],
            datahora=item.get('timestamp'),
            saldo_apos=item.get('saldoApos', 0)
        )
        db.session.add(mov)
        importados += 1
    db.session.commit()
    print(f"Importadas {importados} movimentações.")
