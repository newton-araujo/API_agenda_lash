from src.database.conn import connection_db
from flask import Blueprint,request,jsonify
from src.validations.valid_hour import valid_hour_available
from src.validations.valid_proc_end_hour import valid_procedure_hr_dt_end


scheduling = Blueprint('agendamento', __name__)

@scheduling.post('/agendamento')
def create_new_scheduling():
    
    conn = connection_db()
    cursor = conn.cursor()
    dados = request.get_json()
    
    phone_client = dados.get('phone')
    dt_hr_start = dados.get('dt_start')
    type_proc = dados.get('type_proc')
    status = dados.get('status')
    price = dados.get('price')
    
    dt_hr_end = valid_procedure_hr_dt_end(type_proc,dt_hr_start)
    
    
    if dt_hr_end == 103202:
        return jsonify({
            'message':'procedimento não cadastrado'
        })
    
    
    hours_available = valid_hour_available(dt_hr_start,dt_hr_end)
    
    if hours_available is None:
        return jsonify({
            'message':'Horário indisponivel'
        }),401
    
    try:
        
        query = '''
        
            insert into agendamentos (telefone_cliente, data_hora_inicio, data_hora_fim, tipo_proc, status, valor) 
            values (?, ?, ?, ?, ?, ?)
        
        '''
        
        cursor.execute(query,(phone_client,dt_hr_start,dt_hr_end,type_proc,status, price))
        conn.commit()
        
        return jsonify({
            'messge':'agendamento realizado'
        })
        
    except Exception as e:
        return jsonify({
            'message':f'Erro ao salvar agendamento - {e}'
        })
    
    finally:
        conn.close()
