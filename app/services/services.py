from app.models.models import get_db, fmt_dt
from datetime import datetime


class ProdutoService:
    @staticmethod
    def listar_todos():
        conn = get_db()
        rows = conn.execute("SELECT * FROM produtos ORDER BY categoria, nome").fetchall()
        conn.close()
        return [ProdutoService._row(r) for r in rows]

    @staticmethod
    def buscar_por_id(pid):
        conn = get_db()
        row = conn.execute("SELECT * FROM produtos WHERE id=?", (pid,)).fetchone()
        conn.close()
        if not row:
            return None
        return ProdutoService._row(row)

    @staticmethod
    def criar(d):
        conn = get_db()
        cur = conn.execute(
            "INSERT INTO produtos(nome,categoria,unidade_kg,unidade_sacos,unidade_caixas,preco_kg) VALUES(?,?,?,?,?,?)",
            (d["nome"], d["categoria"], float(d.get("unidade_kg",0)), int(d.get("unidade_sacos",0)),
             int(d.get("unidade_caixas",0)), float(d.get("preco_kg",0)))
        )
        conn.commit()
        pid = cur.lastrowid
        row = conn.execute("SELECT * FROM produtos WHERE id=?", (pid,)).fetchone()
        conn.close()
        return ProdutoService._row(row)

    @staticmethod
    def atualizar(pid, d):
        conn = get_db()
        conn.execute(
            "UPDATE produtos SET nome=?,categoria=?,unidade_kg=?,unidade_sacos=?,unidade_caixas=?,preco_kg=?,atualizado_em=datetime('now') WHERE id=?",
            (d["nome"], d["categoria"], float(d.get("unidade_kg",0)), int(d.get("unidade_sacos",0)),
             int(d.get("unidade_caixas",0)), float(d.get("preco_kg",0)), pid)
        )
        conn.commit()
        row = conn.execute("SELECT * FROM produtos WHERE id=?", (pid,)).fetchone()
        conn.close()
        return ProdutoService._row(row)

    @staticmethod
    def deletar(pid):
        conn = get_db()
        conn.execute("DELETE FROM produtos WHERE id=?", (pid,))
        conn.commit()
        conn.close()

    @staticmethod
    def resumo_estoque():
        conn = get_db()
        rows = conn.execute("SELECT * FROM produtos").fetchall()
        conn.close()
        cats = {}
        for r in rows:
            cat = r["categoria"]
            if cat not in cats:
                cats[cat] = {"total_kg": 0, "total_sacos": 0, "total_caixas": 0, "itens": 0}
            cats[cat]["total_kg"] += r["unidade_kg"]
            cats[cat]["total_sacos"] += r["unidade_sacos"]
            cats[cat]["total_caixas"] += r["unidade_caixas"]
            cats[cat]["itens"] += 1
        return cats

    @staticmethod
    def _row(r):
        return {
            "id": r["id"], "nome": r["nome"], "categoria": r["categoria"],
            "unidade_kg": r["unidade_kg"], "unidade_sacos": r["unidade_sacos"],
            "unidade_caixas": r["unidade_caixas"], "preco_kg": r["preco_kg"],
            "criado_em": fmt_dt(r["criado_em"]), "atualizado_em": fmt_dt(r["atualizado_em"]),
        }


class MovimentoService:
    @staticmethod
    def registrar(d):
        pid = int(d["produto_id"])
        tipo = d["tipo"]
        kg = float(d.get("quantidade_kg", 0))
        sacos = int(d.get("quantidade_sacos", 0))
        caixas = int(d.get("quantidade_caixas", 0))

        conn = get_db()
        produto = conn.execute("SELECT * FROM produtos WHERE id=?", (pid,)).fetchone()
        if not produto:
            conn.close()
            raise ValueError("Produto não encontrado.")

        if tipo == "entrada":
            conn.execute(
                "UPDATE produtos SET unidade_kg=unidade_kg+?,unidade_sacos=unidade_sacos+?,unidade_caixas=unidade_caixas+?,atualizado_em=datetime('now') WHERE id=?",
                (kg, sacos, caixas, pid)
            )
        elif tipo == "saida":
            if produto["unidade_kg"] < kg or produto["unidade_sacos"] < sacos or produto["unidade_caixas"] < caixas:
                conn.close()
                raise ValueError("Estoque insuficiente para realizar a saída.")
            conn.execute(
                "UPDATE produtos SET unidade_kg=unidade_kg-?,unidade_sacos=unidade_sacos-?,unidade_caixas=unidade_caixas-?,atualizado_em=datetime('now') WHERE id=?",
                (kg, sacos, caixas, pid)
            )

        cur = conn.execute(
            "INSERT INTO movimentos(produto_id,tipo,quantidade_kg,quantidade_sacos,quantidade_caixas,observacao) VALUES(?,?,?,?,?,?)",
            (pid, tipo, kg, sacos, caixas, d.get("observacao",""))
        )
        conn.commit()
        mid = cur.lastrowid
        row = conn.execute("SELECT m.*, p.nome AS produto_nome FROM movimentos m JOIN produtos p ON p.id=m.produto_id WHERE m.id=?", (mid,)).fetchone()
        conn.close()
        return MovimentoService._row(row)

    @staticmethod
    def listar(produto_id=None, tipo=None):
        conn = get_db()
        sql = "SELECT m.*, p.nome AS produto_nome FROM movimentos m JOIN produtos p ON p.id=m.produto_id"
        params = []
        filters = []
        if produto_id:
            filters.append("m.produto_id=?"); params.append(produto_id)
        if tipo:
            filters.append("m.tipo=?"); params.append(tipo)
        if filters:
            sql += " WHERE " + " AND ".join(filters)
        sql += " ORDER BY m.data DESC LIMIT 100"
        rows = conn.execute(sql, params).fetchall()
        conn.close()
        return [MovimentoService._row(r) for r in rows]

    @staticmethod
    def _row(r):
        return {
            "id": r["id"], "produto_id": r["produto_id"], "produto_nome": r["produto_nome"],
            "tipo": r["tipo"], "quantidade_kg": r["quantidade_kg"],
            "quantidade_sacos": r["quantidade_sacos"], "quantidade_caixas": r["quantidade_caixas"],
            "observacao": r["observacao"] or "", "data": fmt_dt(r["data"]),
        }


class BalancoService:
    @staticmethod
    def criar(d):
        conn = get_db()
        cur = conn.execute(
            "INSERT INTO balancos(responsavel,observacao) VALUES(?,?)",
            (d.get("responsavel",""), d.get("observacao",""))
        )
        bid = cur.lastrowid
        for item in d.get("itens", []):
            conn.execute(
                "INSERT INTO itens_balanco(balanco_id,produto_nome,categoria,quantidade_kg,quantidade_sacos,quantidade_caixas) VALUES(?,?,?,?,?,?)",
                (bid, item["produto_nome"], item.get("categoria",""),
                 float(item.get("quantidade_kg",0)), int(item.get("quantidade_sacos",0)), int(item.get("quantidade_caixas",0)))
            )
        conn.commit()
        result = BalancoService._fetch(conn, bid)
        conn.close()
        return result

    @staticmethod
    def listar():
        conn = get_db()
        rows = conn.execute("SELECT * FROM balancos ORDER BY data_balanco DESC").fetchall()
        result = [BalancoService._fetch(conn, r["id"]) for r in rows]
        conn.close()
        return result

    @staticmethod
    def buscar_por_id(bid):
        conn = get_db()
        result = BalancoService._fetch(conn, bid)
        conn.close()
        return result

    @staticmethod
    def _fetch(conn, bid):
        b = conn.execute("SELECT * FROM balancos WHERE id=?", (bid,)).fetchone()
        if not b:
            return None
        itens = conn.execute("SELECT * FROM itens_balanco WHERE balanco_id=?", (bid,)).fetchall()
        return {
            "id": b["id"], "data_balanco": fmt_dt(b["data_balanco"]),
            "responsavel": b["responsavel"], "observacao": b["observacao"],
            "itens": [{"id":i["id"],"produto_nome":i["produto_nome"],"categoria":i["categoria"],
                       "quantidade_kg":i["quantidade_kg"],"quantidade_sacos":i["quantidade_sacos"],
                       "quantidade_caixas":i["quantidade_caixas"]} for i in itens]
        }
