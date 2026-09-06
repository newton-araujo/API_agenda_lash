from src.database.conn import connection_db
from flask import Blueprint, request, jsonify



status = Blueprint('status', __name__)


@status.get('/status_proc')
def list_status_proc():
    
    conn = connection_db()
    
    try:
        
        query = ''' select * from status_proc '''
        
        result = conn.execute(query).fetchall()
        
        return jsonify(dict(result)),200
    
    except Exception as e:
        
        return jsonify({
            'message':f'Erro ao buscar status {e}'
        }),401
        
    finally:
        conn.close()