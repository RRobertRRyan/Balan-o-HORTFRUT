import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'hortfrut.db')


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            unidade_kg REAL DEFAULT 0,
            unidade_sacos INTEGER DEFAULT 0,
            unidade_caixas INTEGER DEFAULT 0,
            preco_kg REAL DEFAULT 0,
            criado_em TEXT DEFAULT (datetime('now')),
            atualizado_em TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS movimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            quantidade_kg REAL DEFAULT 0,
            quantidade_sacos INTEGER DEFAULT 0,
            quantidade_caixas INTEGER DEFAULT 0,
            observacao TEXT,
            data TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(produto_id) REFERENCES produtos(id)
        );
        CREATE TABLE IF NOT EXISTS balancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_balanco TEXT DEFAULT (datetime('now')),
            responsavel TEXT,
            observacao TEXT
        );
        CREATE TABLE IF NOT EXISTS itens_balanco (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            balanco_id INTEGER NOT NULL,
            produto_nome TEXT NOT NULL,
            categoria TEXT,
            quantidade_kg REAL DEFAULT 0,
            quantidade_sacos INTEGER DEFAULT 0,
            quantidade_caixas INTEGER DEFAULT 0,
            FOREIGN KEY(balanco_id) REFERENCES balancos(id)
        );
    """)
    # Seed if empty
    count = c.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
    if count == 0:
        seeds = [
            ("Cebola Amarela", "cebola_amarela", 500, 10, 0, 2.50),
            ("Cebola Roxa",    "cebola_roxa",    200, 4,  0, 3.80),
            ("Alho Nacional",  "alho",           150, 0,  5, 15.0),
            ("Cebola Miúda",   "cebola_miuda",   80,  2,  0, 2.00),
        ]
        c.executemany(
            "INSERT INTO produtos(nome,categoria,unidade_kg,unidade_sacos,unidade_caixas,preco_kg) VALUES(?,?,?,?,?,?)",
            seeds
        )
    conn.commit()
    conn.close()


def fmt_dt(s):
    """Format ISO datetime string to DD/MM/YYYY HH:MM"""
    try:
        dt = datetime.strptime(s[:16], "%Y-%m-%dT%H:%M") if "T" in s else datetime.strptime(s[:16], "%Y-%m-%d %H:%M")
        return dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        return s or ""
