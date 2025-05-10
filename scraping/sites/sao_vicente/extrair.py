from selenium.webdriver.common.by import By
from config import URLS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import math
import time
import pandas as pd
import re
from datetime import datetime
data_str = datetime.now().strftime("%Y/%m/%d %H:%M")

departamentos=['Ovos', 'Carnes.-Aves-E-Peixes', 
'Frios-E-Laticínios', 'Empanados', 'Limpeza', 'Creme-De-Leite-1', 'Leite-Condensado-1', 
"Cafés.-Chás-E-Achocolatados","Cestas-Alimentícias-1", "Conservas-E-Enlatados", "Cozinha-Do-Mundo-1", 
"Massas", "Mercearia-Básica", "Molhos-Para-Lanches", "Temperos--E--Molhos-Diversos"]

def get_Links(driver):
    wait=WebDriverWait(driver, timeout=10)
    menu = driver.find_element(By.XPATH, '//*[@id="vueApp"]/header/div/div[7]/div/div[1]/div[1]/div/div[8]')
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", menu)  
    wait.until(EC.element_to_be_clickable((menu)))
    menu.click()
    links=[]
        
    lista_subsubcategorias = menu.find_elements(By.CLASS_NAME, "menudesktop-subsubcategories")
    for subsub in lista_subsubcategorias:
        lista_a=subsub.find_elements(By.XPATH, "./a[not(ancestor::p)]")
        for a in lista_a:
            links.append(a.get_attribute("href"))
            
    df_links = pd.DataFrame(links)
    df_links.to_csv("results/saovicente/lista_links_teste.csv", index=False)


def get_saoVito(driver):
    wait=WebDriverWait(driver, timeout=10)
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

def expandir(driver):
    wait=WebDriverWait(driver, timeout=10)
    s = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="maincontent"]/div[2]/div/div/div/div[1]/div[2]/p')))

    total = int(''.join(filter(str.isdigit, s.text)))
    final_url = math.ceil(total/20) *20
    return str(final_url)


def extrair_produtosSV(driver):
    get_saoVito(driver)
    links = pd.read_csv("results/saovicente/lista_links.csv", header=None)[0].tolist()
    links = [link for link in links if link.startswith("http")]
    dados=[]
    for site in links:
        driver.get(site)
        try:
            driver.get(site+"?sz="+expandir(driver))
        except TimeoutException:
            continue
        container = driver.find_elements(By.CSS_SELECTOR, 'div.productCard__container')

        for cont in container:
            try:
                preco_prod=cont.find_element(By.CSS_SELECTOR, 'span.productPrice__price:not(.lineThrough)').text
            except NoSuchElementException:
                preco_prod=None
            dados.append({
                "Nome": cont.find_element(By.CSS_SELECTOR, 'span.productCard__title').text,
                "Preço": preco_prod,
                "Categoria": driver.find_element(By.CSS_SELECTOR, "div.breadCrumb__content").text,
                "Data": data_str
            })
        df = pd.DataFrame(dados)
        print(df)
    return dados

def testeSV(driver):
    get_saoVito(driver)
    site=["https://www.svicente.com.br/Acougue-Swift", "https://www.svicente.com.br/Aves-Swift-1"]
    dados=[]
    for sit in site:
        driver.get(sit)
        try:
            driver.get(sit+"?sz="+expandir(driver))
        except TimeoutException:
            continue
        container = driver.find_elements(By.CSS_SELECTOR, 'div.productCard__container')

        for cont in container:
            try:
                preco_prod=cont.find_element(By.CSS_SELECTOR, 'span.productPrice__price:not(.lineThrough)').text
            except NoSuchElementException:
                preco_prod=cont.find_element(By.CSS_SELECTOR, "div.promotionTagText__container").text
            dados.append({
                "Nome": cont.find_element(By.CSS_SELECTOR, 'span.productCard__title').text,
                "Preço": preco_prod,
                "Categoria": driver.find_element(By.CSS_SELECTOR, "div.breadCrumb__content").text
            })
        df = pd.DataFrame(dados)
        print(df)
    return dados