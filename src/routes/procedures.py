from src.database.conn import connection_db
from flask import Blueprint, jsonify, request


procedure = Blueprint("procedure", __name__)

# creates a new procedure
@procedure.post('/procedure')
def create_procedure():
    
    conn = connection_db()
    
    if conn is None:
        
        return jsonify({
            'message':'Erro ao se conectar o banco'
        })
        
    
    dados = request.get_json()
    
    cod_proc = dados.get("cod_proc")
    name_proc = dados.get("name_procedure")
    temp_proc = dados.get("temp_procedure")
    price_proc = dados.get("price_procedure")
    
    
    if name_proc is None or temp_proc is None or price_proc is None:
        
        return jsonify({
            'message':'Preencha todos os campos!'
        })
        
    
    try:
        query = '''
            insert into procedimentos (cod_proc ,nome_proc, temp_proc, valor_proc) 
            values (? , ? , ? ,?)
        '''
        
        conn.execute(query, (cod_proc ,name_proc, temp_proc, price_proc))
        
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
        

 # searches for all procedure
@procedure.get('/procedure')
def get_all_procedure():
    
    conn = connection_db()

    try:
        
        query = '''
            select *
            from procedimentos
        '''
        
        dados = conn.execute(query).fetchall()
        
        all_proc = [dict(proc) for proc in dados]
        
        return jsonify(all_proc)
        
    except Exception as e:
        
        return jsonify({
            'messge-get-procedure':f'Erro ao buscar - {e}'
        })
        
    finally:
        conn.close()
        
# looking for a procedure 
@procedure.get('/procedure/<int:cod_proc>')
def get_procedure(cod_proc):
    
    conn = connection_db()
    
    try:
        
        query = '''
            select * 
            from procedimentos
            where cod_proc = ?
        '''
        
        result = conn.execute(query, (cod_proc,)).fetchone()
        
        if result is None:
            
            return jsonify({
                'message':'Nenhum procedimento encontrado'
            })
        
        return jsonify(dict(result))
    
    except Exception as e:
        return jsonify({
            'message-get-procedure':f'Erro ao buscar procedimento - {e}'
        })
        
    finally:
        conn.close()