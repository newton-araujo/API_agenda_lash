from src.database.conn import connection_db
from flask import Blueprint, request, jsonify
from src.validations.valid_hour import valid_hour_available
from src.validations.valid_proc_end_hour import valid_procedure_hr_dt_end

scheduling = Blueprint('agendamento', __name__)

@scheduling.post('/agendamento')
def create_new_scheduling():
    conn = connection_db()
    cursor = conn.cursor()
    dados = request.get_json() or {}
    
    phone_client = dados.get('phone')
    dt_hr_start = dados.get('dt_start')
    type_proc = dados.get('type_proc')
    status = dados.get('status')
    price = dados.get('price')
    
    dt_hr_end = valid_procedure_hr_dt_end(type_proc, dt_hr_start)
    
    if dt_hr_end == 103202:
        conn.close()
        return jsonify({'message': 'procedimento não cadastrado'}), 400
    
    hours_available = valid_hour_available(dt_hr_start, dt_hr_end)
    if hours_available is None:
        conn.close()
        return jsonify({'message': 'Horário indisponivel'}), 401
    
    try:
        query = '''
            insert into agendamentos (telefone_cliente, data_hora_inicio, data_hora_fim, tipo_proc, status, valor) 
            values (?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (phone_client, dt_hr_start, dt_hr_end, type_proc, status, price))
        conn.commit()
        return jsonify({'message': 'agendamento realizado'}), 201
        
    except Exception as e:
        return jsonify({'message': f'Erro ao salvar agendamento - {e}'}), 500
        
    finally:
        conn.close()


@scheduling.get('/agendamento')
def all_scheduling():
    conn = connection_db()
    cursor = conn.cursor()
    
    try:
        query = '''
            select id, telefone_cliente, data_hora_inicio, data_hora_fim, tipo_proc, status, valor 
            from agendamentos
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        
        agendamentos = []
        for row in rows:
            agendamentos.append({
                'id': row[0],
                'phone': row[1],
                'dt_start': row[2],
                'dt_end': row[3],
                'type_proc': row[4],
                'status': row[5],
                'price': row[6]
            })
            
        return jsonify(agendamentos), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro ao listar agendamentos - {e}'}), 500
        
    finally:
        conn.close()


@scheduling.get('/agendamento/<int:id_scheduling>')
def get_scheduling_by_id(id_scheduling):
    conn = connection_db()
    cursor = conn.cursor()
    
    try:
        query = '''
            select id, telefone_cliente, data_hora_inicio, data_hora_fim, tipo_proc, status, valor 
            from agendamentos 
            where id = ?
        '''
        cursor.execute(query, (id_scheduling,))
        row = cursor.fetchone()
        
        if not row:
            return jsonify({'message': 'Agendamento não encontrado'}), 404
            
        agendamento = {
            'id': row[0],
            'phone': row[1],
            'dt_start': row[2],
            'dt_end': row[3],
            'type_proc': row[4],
            'status': row[5],
            'price': row[6]
        }
        return jsonify(agendamento), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro ao buscar agendamento - {e}'}), 500
        
    finally:
        conn.close()


@scheduling.put('/agendamento/<int:id_scheduling>')
def update_scheduling(id_scheduling):
    conn = connection_db()
    cursor = conn.cursor()
    dados = request.get_json() or {}
    
    try:
        cursor.execute('select id, data_hora_inicio, tipo_proc from agendamentos where id = ?', (id_scheduling,))
        current = cursor.fetchone()
        
        if not current:
            return jsonify({'message': 'Agendamento não encontrado'}), 404
        
        phone_client = dados.get('phone')
        dt_hr_start = dados.get('dt_start', current[1])
        type_proc = dados.get('type_proc', current[2])
        status = dados.get('status')
        price = dados.get('price')
        
        # Recalcula e valida horário caso procedimento ou data inicial tenham mudado
        dt_hr_end = valid_procedure_hr_dt_end(type_proc, dt_hr_start)
        if dt_hr_end == 103202:
            return jsonify({'message': 'procedimento não cadastrado'}), 400
        
        if dt_hr_start != current[1] or type_proc != current[2]:
            hours_available = valid_hour_available(dt_hr_start, dt_hr_end)
            if hours_available is None:
                return jsonify({'message': 'Horário indisponivel'}), 401

        query = '''
            update agendamentos 
            set telefone_cliente = ?, data_hora_inicio = ?, data_hora_fim = ?, tipo_proc = ?, status = ?, valor = ?
            where id = ?
        '''
        cursor.execute(query, (phone_client, dt_hr_start, dt_hr_end, type_proc, status, price, id_scheduling))
        conn.commit()
        
        return jsonify({'message': 'Agendamento atualizado com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro ao atualizar agendamento - {e}'}), 500
        
    finally:
        conn.close()


@scheduling.delete('/agendamento/<int:id_scheduling>')
def delete_scheduling(id_scheduling):
    conn = connection_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('select id from agendamentos where id = ?', (id_scheduling,))
        if not cursor.fetchone():
            return jsonify({'message': 'Agendamento não encontrado'}), 404
            
        cursor.execute('delete from agendamentos where id = ?', (id_scheduling,))
        conn.commit()
        
        return jsonify({'message': 'Agendamento excluído com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro ao deletar agendamento - {e}'}), 500
        
    finally:
        conn.close()