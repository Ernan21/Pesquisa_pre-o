from database import *
from colect import *
current_user = 'Lemos Supermercado'
empresas = database.select(f"SELECT * FROM empresas WHERE nome = '{current_user}'")

def main(username, senha, time_wait):
    lojas = database.select('SELECT * FROM lojas WHERE status = 0 limit 1')
    colect.login(username, senha, time_wait)
    for i in lojas:
        print(i[2])
        coleta_preços = colect.colect_prices(i[2], time_wait)

main(empresas[3], empresas[4], empresas[5])