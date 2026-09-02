from src.database.conn import connection_db
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash



users = Blueprint("users",__name__)



#Create new user
@users.post("/users")
def create_user ():

    dados = request.get_json()
    
    user = dados.get("user")
    email = dados.get("email")
    password = dados.get("password")
    
    
    hash_password = generate_password_hash(password)
    
    
    if not user or not email or not password:
        
        return jsonify({
            "erro":"Usuário, email e senha são obrigatórios"
        }),400
    
    
    conn = connection_db()
    
    if conn:
        
        cursor = conn.cursor()
        
        
        query = '''
        
            insert into users (user_name, password, email_user) values (?,?,?)
        
        '''
        
        cursor.execute(query,(user, hash_password, email))
        
        
        conn.commit()
        
        res_user = {
            
            'message':f'Usuário {user} cadastrado com sucesso!'
            
        }
        
        return jsonify(res_user),201

    
    else:
        
        print(conn)

#Get all users
@users.get("/users")
def get_users ():
    
    conn = connection_db()
    cursor = conn.cursor()
    
    
    query = '''select * from users'''
    
    
    result = cursor.execute(query).fetchall()
    
    
    list_users = [dict(user) for user in result]
    
    return jsonify(list_users)
    
#Update password
