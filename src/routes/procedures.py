from src.database.conn import connection_db
from flask import Blueprint, jsonify, request,json


procedure = Blueprint("procedure", __name__)

# creates a new procedure
@procedure.post('/procedure')
def create_procedure():
    
    conn = connection_db()
    
    if conn is None:
        
        return jsonify({
            'message':'Erro ao se conectar o banco'
        }),401
        
    
    dados = request.get_json()
    
    cod_proc = dados.get("cod_proc")
    name_proc = dados.get("name_procedure")
    temp_proc = dados.get("temp_procedure")
    price_proc = dados.get("price_procedure")
    
    
    if name_proc is None or temp_proc is None or price_proc is None:
        
        return jsonify({
            'message':'Preencha todos os campos!'
        }),400
        
    
    try:
        query = '''
            insert into procedimentos (cod_proc ,nome_proc, temp_proc, valor_proc) 
            values (? , ? , ? ,?)
        '''
        
        conn.execute(query, (cod_proc ,name_proc, temp_proc, price_proc))
        
        conn.commit()
        
        return jsonify({
            'message':'Procedimento cadastrado com sucesso!'
        }),200
        
        
    except Exception as e:
        return jsonify({
            'message-erro-proc':f'Erro ao cadastrar procedimentos - {e}'
        }),401
        
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
            }),400
        
        return jsonify(dict(result)),200
    
    except Exception as e:
        return jsonify({
            'message-get-procedure':f'Erro ao buscar procedimento - {e}'
        }),401
        
    finally:
        conn.close()
        
# Updating procedure

@procedure.put('/procedure/<int:cod_proc>')
def updating_procedure(cod_proc):
    
    conn = connection_db()
    
    dados = request.get_json(silent=True)
    
    name_proc = dados.get('nome_proc')
    temp_proc = dados.get('temp_proc')
    price_proc = dados.get('price_proc')
    print(temp_proc)
    
    if name_proc is None or temp_proc is None or price_proc is None:
        
        return jsonify({
            'message':'Preencha todos os campos'
        }),400
    
    try:
        
        query = '''
            
            update procedimentos
            set nome_proc = ?,
                temp_proc = ?,
                valor_proc = ?
            where cod_proc = ?
                
            '''
            
        conn.execute(query,(name_proc, temp_proc, price_proc, cod_proc))
        
        conn.commit()
        
        return jsonify({
            'massge':f'Procedimento {name_proc} atualizado'
        })
    
    except Exception as e:
        
        return jsonify({
            'message':f'Erro ao atualizar procedimento - {e}'
        }),401
        
    finally:
        conn.close()