from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import math

driver_path = 'chromedriver-win64/chromedriver.exe' 
url = 'https://www.svicente.com.br/'

service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service)

departamentos=['Ovos', 'Carnes.-Aves-E-Peixes', 
'Frios-E-Laticínios', 'Empanados', 'Limpeza', 
'Doces-E-Sobremesas']

wait=WebDriverWait(driver, timeout=10)

def get_SaoVito():
    driver.get(url)
    driver.maximize_window()
    link = driver.find_element(By.PARTIAL_LINK_TEXT,'Nova Odessa')
  
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", link)  
    wait.until(EC.element_to_be_clickable((link)))
    link.send_keys(Keys.ENTER)
    cep = driver.find_element(By.XPATH, '//*[@id="new-switch-store-modal"]/div[2]/div/form/div[1]/input')
    numero = driver.find_element(By.XPATH, '//*[@id="new-switch-store-modal"]/div[2]/div/form/div[2]/input')
    enviar = driver.find_element(By.XPATH, '//*[@id="new-switch-store-modal"]/div[2]/div/form/button')
    
    ActionChains(driver)\
        .send_keys_to_element(cep, "13478779")\
        .perform()
    ActionChains(driver)\
        .send_keys_to_element(numero, "155")\
        .perform()
    enviar.click()
    retirar = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="new-switch-store-modal"]/div[2]/div/div[2]/ul/li[1]/p' )))
    retirar.click()
    sao_vito= wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="001"]' )))
    sao_vito.click()
    time.sleep(5)

get_SaoVito()


def listaCompleta():
    # driver.get(url+"Hortifruti-1")
    # driver.maximize_window()
    wait=WebDriverWait(driver, timeout=10)
    s = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="maincontent"]/div[2]/div/div/div/div[1]/div[2]/p')))

    total = int(''.join(filter(str.isdigit, s.text)))
    final_url = math.ceil(total/20) *20
    return str(final_url)
    # for i in range(int(total/20)):
    #     # botao = driver.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div/div/div[2]/div/div[2]/div/button') 
    #     botao = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="maincontent"]/div[2]/div/div/div/div[2]/div/div[2]/div/button')))
    #     driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", botao)  
    #     botao.click()
    #     time.sleep(6)

    print(total)
dados = []
for departamento in departamentos:
    driver.get(url+departamento)
    driver.get(url+departamento+"?sz="+listaCompleta())
    
    titulos = driver.find_elements(By.CSS_SELECTOR, 'span.productCard__title')
    precos = driver.find_elements(By.CSS_SELECTOR, 'span.productPrice__price:not(.lineThrough)')

    for titulo, preco in zip(titulos, precos):
        dados.append({'Título': titulo.text, 'Preço': preco.text, 'Departamento': departamento})

   
df = pd.DataFrame(dados)
print(df)

df.to_csv('titulos_e_precos-teste.csv', index=False)

driver.quit()