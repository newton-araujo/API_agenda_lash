from src.database.conn import connection_db
from flask import Blueprint, jsonify, request


procedure = Blueprint("procedure", __name__)


@procedure.post('/procedure')
def create_procedure():
    
    conn = connection_db()
    
    if conn is None:
        
        return jsonify({
            'message':'Erro ao se conectar o banco'
        })
        
    
    dados = request.get_json()
    
    name_proc = dados.get("name_procedure")
    temp_proc = dados.get("temp_procedure")
    price_proc = dados.get("price_procedure")
    
    
    if name_proc is None or temp_proc is None or price_proc is None:
        
        return jsonify({
            'message':'Preencha todos os campos!'
        })
        
    
    try:
        query = '''
            insert into procedimentos (nome_proc, temp_proc, valor_proc) 
            values (? , ? , ?)
        '''
        
        conn.execute(query, (name_proc, temp_proc, price_proc))
        
        conn.commit()
        
        return jsonify({
            'message':'Procedimento cadastrado com sucesso!'
        })
        
        
    except Exception as e:
        return jsonify({
            'message-erro-proc':f'Erro ao cadastrar procedimentos - {e}'
        })
        
    finally:
        conn.close()