from src.database.conn import connection_db
from datetime import datetime, timedelta
from flask import jsonify

def valid_procedure_hr_dt_end(proc, start_proc):
    
    conn = connection_db()
    cursor = conn.cursor()
    
    formato = "%Y-%m-%d %H:%M:%S"
    start_hour = datetime.strptime(start_proc, formato)
    
    
    try:
        
        query = '''
            select *
            from procedimentos
            where nome_proc = ?
        '''
        
        cursor.execute(query,(proc,))
        result = cursor.fetchone()
        
        if result is None:
            
            return jsonify({
                'erro': 103202
            })
        
        
        temp_proc = result['temp_proc']

        hours, minutes = map(int, temp_proc.split(":"))
        
        hour_end = start_hour + timedelta(hours=hours, minutes=minutes)
        
        return hour_end

    except Exception as e:
        return jsonify({
            'message':f'erro ao buscar procedimento'
        })
