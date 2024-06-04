from database import *
from colect import *
current_user = 'lemos'
empresas = database.select(f"SELECT * FROM empresas WHERE usuario = '{current_user}'")
print(empresas)
for empresa in empresas:
    username = empresa[1][3]
    senha = empresa[1][4]
    time_wait = empresa[1][5]
    lojas = database.select('SELECT * FROM lojas WHERE status = 0 limit 1')
    colect.login(username, senha, time_wait)
    for i in lojas:
        print(i[2])
        coleta_preços = colect.colect_prices(i[2], time_wait)