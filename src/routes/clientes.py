from src.database.conn import connection_db
from flask import Blueprint, request, jsonify

client = Blueprint('client',__name__)

#Create new client
@client.post('/cliente')
def create_new_client ():
    
    conn = connection_db()
    
    try:
        dados = request.get_json()
        
        name_client = dados.get("name")
        phone_client = dados.get("phone")
        
        
        if not name_client or not phone_client:
            
            return jsonify({
                "erro":"Preencha todos os campos"
            }),401
        

        query = '''
            insert into clientes (nome, telefone_client) 
            values (? , ?)
        '''
        
        conn.execute(query,(name_client, phone_client),)
        
        conn.commit()

        
        
        result = {
            "message":f"Cadastro realizado com sucesso!"
        }
        
        return jsonify(result)
        
    
    except Exception as erro:
        
        return jsonify({
            "erro":f"Falha ao cadastrar cliente: {erro}"
        }),500
        
    finally:
        conn.close()
        

#Get clients
@client.get('/cliente/<int:phone>')
def get_client (phone):

    try:  
        conn = connection_db()
        result = conn.execute(
            """
                select * 
                from clientes
                where telefone_client = ?
            """,
            (phone,)
        ).fetchone()
        
        
        if result is None:
            return jsonify({
                "erro":"telefone informando não existe."
            })
        
        
        return jsonify(dict(result))
    
    
    except Exception as erro:
        
        return jsonify({
            "erro":f"Erro interno contate o suporte - {erro}"
        })
    
    finally:
        conn.close()


#Get all clients
@client.get('/cliente')
def get_all_client():
    
    try:
        
        conn = connection_db()
        
        all_clients = conn.execute(
            ''' 
                select *
                from clientes
            '''
        ).fetchall()
        
        
        list_clients = [dict(d_client) for d_client in all_clients]
        
        return jsonify(list_clients)
        
        
    except Exception as erro:
        return jsonify({
            "erro - all_clients":f"Erro interno entre em contato com o suporte - {erro}"
        })
    
    finally:
        conn.close()
        


#Update client
@client.put("/cliente/<int:phone>")
def update_client(phone):
    
    conn = connection_db()
    
    dados = request.get_json()
    
    name_client = dados.get("name")
    
    print(name_client)
    
    #Client exists
    
    client_exists = conn.execute(
        
        '''
            select * 
            from clientes 
            where telefone_client = ?
            
        ''',
        (phone,)
    ).fetchone()
    
    
    if client_exists is None:
        
        conn.close()
        
        return jsonify({
            "error":"cliente não localizado"
        })
    
    
    #If the client exists, update it
    try:
        
        conn.execute(
            '''
                update clientes
                set nome = ?
                where telefone_client = ?
            ''',
            
            (name_client, phone)
            
            )
        
        conn.commit()
        
        return jsonify({
            'message':f"cliente - {name_client} atualziado"
        })
    except Exception as e:
        
        return jsonify({
            'er1o - update_client':'Entre em contato com o suporte'
        }),400
        
    finally:
        conn.close()
    
    
    
    