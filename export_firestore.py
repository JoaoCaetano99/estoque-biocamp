import json
import os
from google.cloud import firestore

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "serviceAccount.json"

db = firestore.Client()

def serialize_firestore(obj):
    # Ajusta para serializar datas dos tipos mais comuns do Firestore
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    return str(obj)

# Exporta coleção produtos
produtos_ref = db.collection('produtos')
produtos = []
for doc in produtos_ref.stream():
    data = doc.to_dict()
    data['id'] = doc.id
    produtos.append(data)

with open('produtos_firestore.json', 'w', encoding='utf-8') as f:
    json.dump(produtos, f, ensure_ascii=False, indent=2, default=serialize_firestore)

print('Exportados:', len(produtos), 'produtos.')

# Exporta coleção movimentacoes
movs_ref = db.collection('movimentacoes')
movs = []
for doc in movs_ref.stream():
    data = doc.to_dict()
    data['id'] = doc.id
    movs.append(data)

with open('movimentacoes_firestore.json', 'w', encoding='utf-8') as f:
    json.dump(movs, f, ensure_ascii=False, indent=2, default=serialize_firestore)

print('Exportados:', len(movs), 'movimentações.')
