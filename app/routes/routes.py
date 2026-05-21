from flask import Blueprint, jsonify, request, render_template
from app.services.services import ProdutoService, MovimentoService, BalancoService

main_bp = Blueprint("main", __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")


# ─── Pages ──────────────────────────────────────────────────────────────────
@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/estoque")
def estoque():
    return render_template("estoque.html")

@main_bp.route("/movimentos")
def movimentos():
    return render_template("movimentos.html")

@main_bp.route("/balanco")
def balanco():
    return render_template("balanco.html")


# ─── API: Produtos ───────────────────────────────────────────────────────────
@api_bp.route("/produtos", methods=["GET"])
def get_produtos():
    return jsonify(ProdutoService.listar_todos())

@api_bp.route("/produtos", methods=["POST"])
def post_produto():
    dados = request.get_json()
    try:
        return jsonify(ProdutoService.criar(dados)), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@api_bp.route("/produtos/<int:pid>", methods=["PUT"])
def put_produto(pid):
    dados = request.get_json()
    try:
        return jsonify(ProdutoService.atualizar(pid, dados))
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@api_bp.route("/produtos/<int:pid>", methods=["DELETE"])
def delete_produto(pid):
    ProdutoService.deletar(pid)
    return jsonify({"mensagem": "Produto removido."})

@api_bp.route("/produtos/resumo", methods=["GET"])
def resumo_estoque():
    return jsonify(ProdutoService.resumo_estoque())


# ─── API: Movimentos ─────────────────────────────────────────────────────────
@api_bp.route("/movimentos", methods=["GET"])
def get_movimentos():
    pid = request.args.get("produto_id", type=int)
    tipo = request.args.get("tipo")
    return jsonify(MovimentoService.listar(produto_id=pid, tipo=tipo))

@api_bp.route("/movimentos", methods=["POST"])
def post_movimento():
    dados = request.get_json()
    try:
        return jsonify(MovimentoService.registrar(dados)), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": str(e)}), 400


# ─── API: Balanço ────────────────────────────────────────────────────────────
@api_bp.route("/balancos", methods=["GET"])
def get_balancos():
    return jsonify(BalancoService.listar())

@api_bp.route("/balancos", methods=["POST"])
def post_balanco():
    dados = request.get_json()
    try:
        return jsonify(BalancoService.criar(dados)), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@api_bp.route("/balancos/<int:bid>", methods=["GET"])
def get_balanco(bid):
    b = BalancoService.buscar_por_id(bid)
    if not b:
        return jsonify({"erro": "Não encontrado"}), 404
    return jsonify(b)
