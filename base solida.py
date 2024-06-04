import os, shutil, logging, time
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Acesso ao site
USERNAME = "lemos"
SENHA = "lemos"

# Função para coletar data atual
yesterday_date = datetime.now().strftime("%d-%m-%Y")

# Lojas pesquisadas
loja_pesquisa = [
    {"pesquisa":"Super Telefrango - Joao XXIII ** PARCERIA", "loja":"Super Telefrango - Joao XXIII PARCERIA"},
    {"pesquisa":"Supermercado N. S. Fatima - Maracanau ** UNIFORCA","loja":"Supermercado N. S. Fatima - Maracanau UNIFORCA"},
    {"pesquisa":"Super Vilton ** PARCERIA","loja":"Super Vilton PARCERIA"},
    {"pesquisa":"R Center - Parque Santa Rosa ** UNIFORCA","loja":"R Center - Parque Santa Rosa UNIFORCA"},
    {"pesquisa":"Claeck Supermercados ** INTEGRADA","loja":"Claeck Supermercados INTEGRADA"}
]

# loja_pesquisa = [{"pesquisa":"Super Telefrango - Joao XXIII ** PARCERIA", "loja":"Super Telefrango - Joao XXIII PARCERIA"}]

# Faz login no site
def login(driver, username, senha, time_wait):
    try:
        """Log in to the website."""
        print("Fazendo login no site")
        driver.get("https://mobile.integraofertas.com.br/login.php")
        WebDriverWait(driver, time_wait).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="usuario"]')))
        driver.find_element(By.XPATH, '//*[@id="usuario"]').send_keys(username)
        driver.find_element(By.XPATH, '//*[@id="senha"]').send_keys(senha)
        driver.find_element(By.XPATH, '//*[@id="btnSubmit"]').click()
        print("Logado com sucesso")
    except Exception as e:
        exit

# Cria as planilhas com os preços
def colect_prices(driver, loja_name, time_wait):
    try:
        """Go to form's in the website"""
        driver.get("https://mobile.integraofertas.com.br/pesquisa_concorrente.php")
        WebDriverWait(driver, time_wait).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="formPesquisa"]/div/div[1]/span/span[1]/span')))
        # Wait for the preloader to disappear
        WebDriverWait(driver, time_wait).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="produtosPesquisa_info"]')))
        """Coloca a exibição com todos os itens"""
        driver.find_element(By.XPATH, '//*[@id="produtosPesquisa_wrapper"]/div[1]/button[1]/span').click()
        driver.find_element(By.XPATH, '//*[@id="produtosPesquisa_wrapper"]/div[1]/div[2]/div/button[6]/span').click()
        """Colocando a empresa especifica"""
        WebDriverWait(driver, time_wait).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="produtosPesquisa"]/tbody/tr/td'))) # Espera a tabela ser completada
        driver.find_element(By.XPATH, '//*[@id="formPesquisa"]/div/div[1]/span/span[1]/span').click()
        driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input').send_keys(f"{loja_name}\ue007")
        print(f'Pesquisando pela loja {loja_name}')
        WebDriverWait(driver, time_wait).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="produtosPesquisa"]/tbody/tr[2]/td[2]'))) # Espera a tabela ser completada
        driver.find_element(By.XPATH, '//*[@id="produtosPesquisa_wrapper"]/div[1]/button[3]').click()
        
        return True
    except Exception as e:
        print(f"Um erro foi encontrado: {e}")
        return False

# Move os arquivos para o local de armazenamento
def estorage_align(yesterday_date, Loja_name):
    
    """Rename and move files."""
    src = f"c:\\users\\{os.environ['USERNAME']}\\Downloads\\xlsx.xlsx"
    dest = f"c:\\users\\{os.environ['USERNAME']}\\Downloads\\{Loja_name}.xlsx"
    
    while not os.path.exists(src):
        logging.info(f"Wait for file {src}")
        time.sleep(10)

    try:
        os.rename(src, dest)
        logging.info("File renamed successfully.")
        print("File renamed successfully.")
    except Exception as e:
        logging.error(f"An error occurred while renaming the file: {e}")
        print(f"An error occurred while renaming the file: {e}")

    try:
        shutil.move(dest, fr"\\192.168.0.100\documentos\CPD\ERNANDO\..projetos\pesquisa_preço\{yesterday_date}\{Loja_name}.xlsx")
        logging.info("File moved successfully.")
        print("arquivo movido com sucesso")
    except Exception as e:
        logging.error(f"An error occurred while moving the file: {e}")
        print(f"An error occurred while moving the file: {e}")

# Cria os arquivos para serem importados
def converter_para_texto(diretorio):
    for arquivo in os.listdir(diretorio):
        try:
            if arquivo.endswith('.xlsx') or arquivo.endswith('.xls'):
                planilha = pd.read_excel(os.path.join(diretorio, arquivo), usecols='B:C', skiprows=2)
                texto = planilha.to_csv(index=False, sep=';', decimal=',', encoding="UTF-8")
                with open(os.path.join(diretorio, f"{os.path.splitext(arquivo)[0]}.txt"), 'w', encoding='utf-8') as f:
                    f.write(texto)
            print(f"{os.path.splitext(arquivo)[0]}.txt criado com sucesso")
            logging.info(f"{os.path.splitext(arquivo)[0]}.txt criado com sucesso")
        except Exception as e:
            logging.error(f"Um erro foi encontrado: {e}")
            print(f"Um erro foi encontrado: {e}")

# Função principal para executar os comandos em cascata
def main():
    time_wait = 120
    try:
        os.mkdir(fr"\\192.168.0.100\documentos\CPD\ERNANDO\..projetos\pesquisa_preço\{yesterday_date}")
    except Exception as e:
        print(f"Um erro foi encontrado: {e}")
    finally:
        logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        driver = webdriver.Chrome(options=options)
    try:
        login(driver, USERNAME, SENHA, time_wait)
        for i in loja_pesquisa:
            coleta_preços = colect_prices(driver, i['pesquisa'], time_wait)
            time.sleep(20)
            if coleta_preços == True:
                estorage_align(yesterday_date, i['loja'])
                print(f"Pesquisa da loja {i['loja']} feite com sucesso")
    except Exception as e:
        print(f"Um erro foi encontrado: {e}")
    finally:
        driver.quit()
        converter_para_texto(fr"\\192.168.0.100\documentos\CPD\ERNANDO\..projetos\pesquisa_preço\{yesterday_date}")

if __name__ == "__main__":
    main()
    abrir = os.system(fr'explorer \\192.168.0.100\documentos\CPD\ERNANDO\..projetos\pesquisa_preço\{yesterday_date}')
    if abrir == 1:
        print("Abrindo pastas com os preços")
    else:
        print("Erro ao tentar abrir a pasta")