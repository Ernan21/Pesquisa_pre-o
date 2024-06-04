from sqlite3 import *
from erromsg import *
from os import getcwd, mkdir, path
from pathlib import Path

class database:
    class __init__():
        # Cria pasta de configurações se ela não existir
        config_locate = Path(f'{getcwd()}\\config')
        if path.exists(config_locate): pass
        else: mkdir(config_locate)
        
        # Cria banco de dados caso ele não exista e faz um comunicação
        global conx, conn
        try:
            conn = connect(f'{getcwd()}\\config\\db')
            conx = conn.cursor()            
            conn.execute('''
                         CREATE TABLE IF NOT EXISTS lojas (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             nome TEXT,
                             pesquisa TEXT,
                             status INT
                         );
                         ''')
            conn.execute('''
                         CREATE TABLE IF NOT EXISTS empresas (
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             nome TEXT NOT NULL,
                             usuario TEXT NOT NULL,
                             senha TEXT NOT NULL,
                             time_wait INT NOT NULL)
                         ''')
            conn.commit()
        except Exception as e:
            msg.error("ERROR", F'{e}', 5)

    def select(query):
        try:
            result = conx.execute(query).fetchall()
            return result
        except OperationalError as e:
            msg.error( "ERROR", F'{e}', 0)

    def update(query):
        try:
            conx.execute(query)
            conn.commit()
        except Exception as e:
            msg.error( "ERROR", F'{e}', 0)