from src.database.conn import connection_db
from flask import Blueprint, request, jsonify
from src.validations.valid_hour import valid_hour_available
from src.validations.valid_proc_end_hour import valid_procedure_hr_dt_end

agendamento = Blueprint('agendamento', __name__)

def get_columns_map(cursor):
    """
    Inspeciona a tabela agendamentos no banco em execução
    e mapeia os nomes de colunas reais existentes.
    """
    cursor.execute("PRAGMA table_info(agendamentos)")
    cols = [row[1] for row in cursor.fetchall()]
    
    # Identifica chave primária
    pk = 'cod_agendamento' if 'cod_agendamento' in cols else ('id' if 'id' in cols else 'rowid')
    
    # Identifica campos de data/hora
    has_split_date = 'data' in cols and 'horario' in cols
    has_dt_range = 'data_hora_inicio' in cols and 'data_hora_fim' in cols
    
    return {
        'columns': cols,
        'pk': pk,
        'has_split_date': has_split_date,
        'has_dt_range': has_dt_range
    }


@agendamento.get('/agendamento/schema')
def inspect_schema():
    """Endpoint de diagnóstico para inspecionar as colunas do banco atual."""
    conn = connection_db()
    cursor = conn.cursor()
    try:
        schema_info = get_columns_map(cursor)
        return jsonify(schema_info), 200
    except Exception as e:
        return jsonify({'message': f'Erro ao ler schema: {e}'}), 500
    finally:
        conn.close()


@agendamento.post('/agendamento')
def create_new_scheduling():
    conn = connection_db()
    cursor = conn.cursor()
    dados = request.get_json() or {}
    
    phone_client = dados.get('phone')
    type_proc = dados.get('type_proc')
    status = dados.get('status')
    price = dados.get('price')
    
    # Suporta tanto { data, horario } quanto { dt_start }
    date_val = dados.get('data')
    hour_val = dados.get('horario')
    dt_hr_start = dados.get('dt_start')
    
    if not dt_hr_start and date_val and hour_val:
        dt_hr_start = f"{date_val} {hour_val}"
    
    dt_hr_end = valid_procedure_hr_dt_end(type_proc, dt_hr_start)
    if dt_hr_end == 103202:
        conn.close()
        return jsonify({'message': 'procedimento não cadastrado'}), 400
    
    hours_available = valid_hour_available(dt_hr_start, dt_hr_end)
    if hours_available is None:
        conn.close()
        return jsonify({'message': 'Horário indisponivel'}), 401
    
    try:
        schema = get_columns_map(cursor)
        
        if schema['has_split_date']:
            # Estrutura: cod_agendamento, telefone_cliente, data, horario, tipo_proc, status, valor
            dt_part = date_val if date_val else (dt_hr_start.split()[0] if dt_hr_start else '')
            hr_part = hour_val if hour_val else (dt_hr_start.split()[1] if dt_hr_start and ' ' in dt_hr_start else '')
            query = '''
                insert into agendamentos (telefone_cliente, data, horario, tipo_proc, status, valor) 
                values (?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(query, (phone_client, dt_part, hr_part, type_proc, status, price))
        else:
            # Estrutura: data_hora_inicio, data_hora_fim
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


@agendamento.get('/agendamento')
def all_scheduling():
    conn = connection_db()
    cursor = conn.cursor()
    
    try:
        schema = get_columns_map(cursor)
        pk = schema['pk']
        
        if schema['has_split_date']:
            query = f'''
                select {pk}, telefone_cliente, data, horario, tipo_proc, status, valor 
                from agendamentos
            '''
            cursor.execute(query)
            rows = cursor.fetchall()
            agendamentos = [{
                'id': row[0],
                'phone': row[1],
                'data': row[2],
                'horario': row[3],
                'type_proc': row[4],
                'status': row[5],
                'price': row[6]
            } for row in rows]
        else:
            query = f'''
                select {pk}, telefone_cliente, data_hora_inicio, data_hora_fim, tipo_proc, status, valor 
                from agendamentos
            '''
            cursor.execute(query)
            rows = cursor.fetchall()
            agendamentos = [{
                'id': row[0],
                'phone': row[1],
                'dt_start': row[2],
                'dt_end': row[3],
                'type_proc': row[4],
                'status': row[5],
                'price': row[6]
            } for row in rows]
            
        return jsonify(agendamentos), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro ao listar agendamentos - {e}'}), 500
    finally:
        conn.close()


@agendamento.get('/agendamento/<int:id_scheduling>')
def get_scheduling_by_id(id_scheduling):
    conn = connection_db()
    cursor = conn.cursor()
    
    try:
        schema = get_columns_map(cursor)
        pk = schema['pk']
        
        if schema['has_split_date']:
            query = f'''
                select {pk}, telefone_cliente, data, horario, tipo_proc, status, valor 
                from agendamentos 
                where {pk} = ?
            '''
            cursor.execute(query, (id_scheduling,))
            row = cursor.fetchone()
            if not row:
                return jsonify({'message': 'Agendamento não encontrado'}), 404
            
            return jsonify({
                'id': row[0],
                'phone': row[1],
                'data': row[2],
                'horario': row[3],
                'type_proc': row[4],
                'status': row[5],
                'price': row[6]
            }), 200
        else:
            query = f'''
                select {pk}, telefone_cliente, data_hora_inicio, data_hora_fim, tipo_proc, status, valor 
                from agendamentos 
                where {pk} = ?
            '''
            cursor.execute(query, (id_scheduling,))
            row = cursor.fetchone()
            if not row:
                return jsonify({'message': 'Agendamento não encontrado'}), 404
            
            return jsonify({
                'id': row[0],
                'phone': row[1],
                'dt_start': row[2],
                'dt_end': row[3],
                'type_proc': row[4],
                'status': row[5],
                'price': row[6]
            }), 200
            
    except Exception as e:
        return jsonify({'message': f'Erro ao buscar agendamento - {e}'}), 500
    finally:
        conn.close()


@agendamento.put('/agendamento/<int:id_scheduling>')
def update_scheduling(id_scheduling):
    conn = connection_db()
    cursor = conn.cursor()
    dados = request.get_json() or {}
    
    try:
        schema = get_columns_map(cursor)
        pk = schema['pk']
        
        if schema['has_split_date']:
            cursor.execute(f'select {pk}, data, horario, tipo_proc from agendamentos where {pk} = ?', (id_scheduling,))
            current = cursor.fetchone()
            if not current:
                return jsonify({'message': 'Agendamento não encontrado'}), 404
            
            phone_client = dados.get('phone')
            date_proc = dados.get('data', current[1])
            hour_proc = dados.get('horario', current[2])
            type_proc = dados.get('type_proc', current[3])
            status = dados.get('status')
            price = dados.get('price')
            
            dt_hr_start = f"{date_proc} {hour_proc}"
            dt_hr_end = valid_procedure_hr_dt_end(type_proc, dt_hr_start)
            if dt_hr_end == 103202:
                return jsonify({'message': 'procedimento não cadastrado'}), 400
            
            if date_proc != current[1] or hour_proc != current[2] or type_proc != current[3]:
                hours_available = valid_hour_available(dt_hr_start, dt_hr_end)
                if hours_available is None:
                    return jsonify({'message': 'Horário indisponivel'}), 401

            query = f'''
                update agendamentos 
                set telefone_cliente = ?, data = ?, horario = ?, tipo_proc = ?, status = ?, valor = ?
                where {pk} = ?
            '''
            cursor.execute(query, (phone_client, date_proc, hour_proc, type_proc, status, price, id_scheduling))
        else:
            cursor.execute(f'select {pk}, data_hora_inicio, tipo_proc from agendamentos where {pk} = ?', (id_scheduling,))
            current = cursor.fetchone()
            if not current:
                return jsonify({'message': 'Agendamento não encontrado'}), 404
            
            phone_client = dados.get('phone')
            dt_hr_start = dados.get('dt_start', current[1])
            type_proc = dados.get('type_proc', current[2])
            status = dados.get('status')
            price = dados.get('price')
            
            dt_hr_end = valid_procedure_hr_dt_end(type_proc, dt_hr_start)
            if dt_hr_end == 103202:
                return jsonify({'message': 'procedimento não cadastrado'}), 400
            
            if dt_hr_start != current[1] or type_proc != current[2]:
                hours_available = valid_hour_available(dt_hr_start, dt_hr_end)
                if hours_available is None:
                    return jsonify({'message': 'Horário indisponivel'}), 401

            query = f'''
                update agendamentos 
                set telefone_cliente = ?, data_hora_inicio = ?, data_hora_fim = ?, tipo_proc = ?, status = ?, valor = ?
                where {pk} = ?
            '''
            cursor.execute(query, (phone_client, dt_hr_start, dt_hr_end, type_proc, status, price, id_scheduling))

        conn.commit()
        return jsonify({'message': 'Agendamento atualizado com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro ao atualizar agendamento - {e}'}), 500
    finally:
        conn.close()


@agendamento.delete('/agendamento/<int:id_scheduling>')
def delete_scheduling(id_scheduling):
    conn = connection_db()
    cursor = conn.cursor()
    
    try:
        schema = get_columns_map(cursor)
        pk = schema['pk']
        
        cursor.execute(f'select {pk} from agendamentos where {pk} = ?', (id_scheduling,))
        if not cursor.fetchone():
            return jsonify({'message': 'Agendamento não encontrado'}), 404
            
        cursor.execute(f'delete from agendamentos where {pk} = ?', (id_scheduling,))
        conn.commit()
        return jsonify({'message': 'Agendamento excluído com sucesso'}), 200
        
    except Exception as e:
        return jsonify({'message': f'Erro ao deletar agendamento - {e}'}), 500
    finally:
        conn.close()