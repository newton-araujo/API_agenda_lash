from datetime import datetime
from src.database.conn import connection_db


def valid_hour_available(dt_hour_start, dt_hour_end):

    conn = connection_db()
    cursor = conn.cursor()

    formato = "%Y-%m-%d %H:%M:%S"

    try:

        if isinstance(dt_hour_start, str):
            start_hour = datetime.strptime(dt_hour_start, formato)
        else:
            start_hour = dt_hour_start

        if isinstance(dt_hour_end, str):
            end_hour = datetime.strptime(dt_hour_end, formato)
        else:
            end_hour = dt_hour_end

        query = """
            SELECT *
            FROM agendamentos
            WHERE data_hora_inicio < ?
              AND data_hora_fim > ?
        """

        cursor.execute(
            query,
            (
                end_hour,
                start_hour
            )
        )

        result = cursor.fetchone()

        if result:
            return None

        return True

    except Exception as e:
        print(f"Erro ao validar horário: {e}")
        return None

    finally:
        conn.close()
