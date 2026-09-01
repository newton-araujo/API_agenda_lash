import sqlite3 as sq

DB = 'database.db'

def connection_db ():
    
    try:
        
        conn = sq.connect(DB)
        conn.row_factory = sq.Row
        
        return conn
    
    except sq.Error as e:
        
        return f"Erro: {e}"
    