# estoque-biocamp

Sistema de controle de estoque web com autenticação, níveis de acesso (admin/usuário), rodando em Flask + Postgres (Railway).

## Estrutura

- **Usuários admin**: podem criar produtos, visualizar e editar tudo.
- **Usuários comuns**: apenas movimentam e visualizam estoque.
- **Banco:** PostgreSQL (Railway ou local)
- **Backend:** Flask
- **Frontend:** Templates HTML simples (pode evoluir para React futuramente)

## Como usar

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
