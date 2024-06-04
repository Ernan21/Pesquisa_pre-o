from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class colect:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        self.driver = webdriver.Chrome(options=options)
        
    # Faz login no site
    def login(self, username, senha, time_wait):
        try:
            """Log in to the website."""
            print("Fazendo login no site")
            self.driver.get("https://mobile.integraofertas.com.br/login.php")
            WebDriverWait(self.driver, time_wait).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="usuario"]')))
            self.driver.find_element(By.XPATH, '//*[@id="usuario"]').send_keys(username)
            self.driver.find_element(By.XPATH, '//*[@id="senha"]').send_keys(senha)
            self.driver.find_element(By.XPATH, '//*[@id="btnSubmit"]').click()
            print("Logado com sucesso")
        except Exception as e:
            print(f"Erro ao fazer login: {e}")

    # Cria as planilhas com os preços
    def colect_prices(self, loja_name, time_wait):
        try:
            """Go to form's in the website"""
            self.driver.get("https://mobile.integraofertas.com.br/pesquisa_concorrente.php")
            WebDriverWait(self.driver, time_wait).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="formPesquisa"]/div/div[1]/span/span[1]/span')))
            # Wait for the preloader to disappear
            WebDriverWait(self.driver, time_wait).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="produtosPesquisa_info"]')))
            """Coloca a exibição com todos os itens"""
            self.driver.find_element(By.XPATH, '//*[@id="produtosPesquisa_wrapper"]/div[1]/button[1]/span').click()
            self.driver.find_element(By.XPATH, '//*[@id="produtosPesquisa_wrapper"]/div[1]/div[2]/div/button[6]/span').click()
            """Colocando a empresa especifica"""
            WebDriverWait(self.driver, time_wait).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="produtosPesquisa"]/tbody/tr/td'))) # Espera a tabela ser completada
            self.driver.find_element(By.XPATH, '//*[@id="formPesquisa"]/div/div[1]/span/span[1]/span').click()
            self.driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input').send_keys(f"{loja_name}\ue007")
            print(f'Pesquisando pela loja {loja_name}')
            WebDriverWait(self.driver, time_wait).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="produtosPesquisa"]/tbody/tr[2]/td[2]'))) # Espera a tabela ser completada
            self.driver.find_element(By.XPATH, '//*[@id="produtosPesquisa_wrapper"]/div[1]/button[3]').click()

            return True
        except Exception as e:
            print(f"Um erro foi encontrado: {e}")
            return False
