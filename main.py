from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
import time

driver_path = 'chromedriver-win64/chromedriver.exe'  # Substitua pelo caminho do seu WebDriver
url = 'https://www.svicente.com.br/'

service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service)

# driver.get(url)

# time.sleep(5)  # Ajuste o tempo conforme necessário
# botao =driver.find_element(By.XPATH,'//*[@id="vueApp"]/header/div/div[7]/div/div[1]/div[1]/div/div[8]/div[1]')
# ActionChains(driver).move_to_element(botao).pause(1).context_click(botao)

departamentos=['Mercearia', 'Bebidas-', 'Bebidas-Alcoólicas', 'Hortifruti-1', 'Carnes.-Aves-E-Peixes', 
'Frios-E-Laticínios', 'Congelados', 'Higiene-E-Beleza', 'Limpeza', 'Biscoitos-E-Salgadinhos', 
'Doces-E-Sobremesas', 'Padaria', 'Saudáveis-E-Ôrganicos', 'Bazar-E-Utilidades']

for departamento in departamentos:
    driver.get(url+departamento)
    titulos = driver.find_elements(By.CSS_SELECTOR, 'span.productCard__title')
    precos = driver.find_elements(By.CSS_SELECTOR, 'span.productPrice__price:not(.lineThrough)')
    
    dados = []
    for titulo, preco in zip(titulos, precos):
        dados.append({'Título': titulo.text, 'Preço': preco.text, 'Departamento': departamento})
    df = pd.DataFrame(dados)
    print(df)

# Salva o DataFrame em um arquivo CSV (opcional)
# df.to_csv('titulos_e_precos.csv', index=False)

# Fecha o navegador
driver.quit()