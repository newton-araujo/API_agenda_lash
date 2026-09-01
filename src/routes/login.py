from src.database.conn import connection_db
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash


login_auth = Blueprint('login_auth', __name__)


@login_auth.post('/login')
def auth_access():

    conn = connection_db()

    try:
        dados = request.get_json()

        user_get = dados.get("user")
        password_get = dados.get("password")

        if not user_get or not password_get:
            return jsonify({
                "erro": "Usuário e senha são obrigatórios"
            }), 400

        query = """
            SELECT *
            FROM users
            WHERE user_name = ?
        """

        result = conn.execute(
            query,
            (user_get,)
        ).fetchone()

        if result is None:
            return jsonify({
                "erro": "Usuário ou senha inválidos"
            }), 401

        password_valid = check_password_hash(
            result["password"],
            password_get
        )

        if not password_valid:
            return jsonify({
                "erro": "Usuário ou senha inválidos"
            }), 401

        return jsonify({
            "message": "Login realizado com sucesso"
        }), 200

    except Exception as erro:

        print(erro)

        return jsonify({
            "erro": "Erro interno ao realizar login"
        }), 500

    finally:
        conn.close()