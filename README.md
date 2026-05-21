# 🧅 HortFrut HORT — Sistema de Controle de Estoque

Sistema web para controle de estoque e balanço de produtos hortifrutigranjeiros.
Inspirado na identidade visual da **Villefort** (amarelo, vermelho, pontilhado).

## 🏗️ Estrutura em Camadas

```
hortfrut/
├── run.py                        # Entry point
├── requirements.txt
└── app/
    ├── __init__.py               # App factory (create_app)
    ├── extensions.py             # SQLAlchemy instance
    ├── models/
    │   └── models.py             # Camada de Dados (ORM)
    ├── services/
    │   └── services.py           # Camada de Negócio
    ├── routes/
    │   └── routes.py             # Camada de Apresentação (API + Views)
    ├── templates/                # HTML (Jinja2)
    │   ├── base.html
    │   ├── index.html            # Dashboard
    │   ├── estoque.html
    │   ├── movimentos.html
    │   └── balanco.html
    └── static/
        ├── css/style.css
        └── js/app.js
```

## 🚀 Como Rodar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Rodar a aplicação
python run.py

# 3. Acessar no navegador
http://localhost:5000
```

## ✨ Funcionalidades

- **Dashboard** — visão geral do estoque por categoria com últimos movimentos
- **Estoque** — CRUD completo de produtos (Cebola Amarela, Cebola Roxa, Alho, Cebola Miúda)
- **Movimentos** — registros de entrada e saída com atualização automática do estoque
- **Balanço** — formulário de balanço periódico com geração de PDF para impressão

## 📦 Produtos suportados

| Produto | KG | Sacos | Caixas |
|---|---|---|---|
| Cebola Amarela | ✅ | ✅ | — |
| Cebola Roxa | ✅ | ✅ | — |
| Alho | ✅ | — | ✅ |
| Cebola Miúda | ✅ | ✅ | — |

## 🗄️ Banco de Dados

SQLite local (`instance/hortfrut.db`) — sem necessidade de configuração adicional.
Produtos de exemplo são inseridos automaticamente na primeira execução.
