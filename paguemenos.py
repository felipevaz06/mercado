from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import math

driver_path = 'chromedriver-win64/chromedriver.exe' 
url = 'https://www.superpaguemenos.com.br/'

service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service)

driver.get(url)
driver.maximize_window()
wait=WebDriverWait(driver, timeout=10)
link = driver.find_element(By.XPATH, '//*[@id="main-wrapper"]/header/div[3]/div[1]/div[1]/span/span/span')
driver.execute_script("arguments[0].scrollIntoView({block: 'center'})", link)  
wait.until(EC.element_to_be_clickable((link)))
link.click()

def get_Links():
    links=[]
    wait = WebDriverWait(driver, 10)
    lista_categorias = driver.find_elements(By.CSS_SELECTOR, "li.child.level-0")
    lista_textos = [element.text for element in lista_categorias]
    print(lista_textos)

    for item in lista_categorias:
        ActionChains(driver)\
        .move_to_element(item)\
        .perform()
        sub = item.find_element(By.CLASS_NAME, "sub")
        lista_subcategorias = sub.find_elements(By.CSS_SELECTOR, "li.child.level-1, li.level-1")

        for subitem in lista_subcategorias:
            ActionChains(driver)\
        .move_to_element(subitem)\
        .perform()
            sub2=subitem.find_element(By.TAG_NAME, "a")
            if(sub2.get_attribute("href")=="https://www.superpaguemenos.com.br/9616-utilidades-domesticas/"):
                links.append("https://www.superpaguemenos.com.br/bazar/descartaveis/")
            else:
                links.append(sub2.get_attribute("href"))

    print(links)
    df_links = pd.DataFrame(links)
    df_links.to_csv("results/paguemenos/lista_links.csv", index=False)



def get_Produtos():
    links = pd.read_csv("results/paguemenos/lista_links.csv", header=None)[0].tolist()
    links = [link for link in links if link.startswith("http")]
    marcas=[]
    nomes=[]
    precos=[]
    dados=[]
    dados_prod={}
    categorias=[]
    for site in links:
        driver.get(site)
        try:
            texto=driver.find_element(By.CSS_SELECTOR, 'div.text-center.pt-3').text
        except NoSuchElementException:
            continue
        total=int(''.join(filter(str.isdigit, texto)))
        print(total)
        lista_produtos=driver.find_elements(By.CSS_SELECTOR, "div.desc.position-relative")
        for i, produto in enumerate(lista_produtos):
            try:
                preco_prod=produto.find_element(By.CSS_SELECTOR,"p.sale-price").text
            except NoSuchElementException:
                preco_prod = 0
            dados.append({
                "Nome": produto.find_element(By.CSS_SELECTOR, "h2.title").text,
                "Preço": preco_prod,
                "Marca": produto.find_element(By.CSS_SELECTOR, "span.font-size-11.text-primary.font-weight-bold").text,
                "Categoria": driver.find_element(By.CSS_SELECTOR, "h1.h3").text
            })
    df_produtos = pd.DataFrame(dados)
    print(df_produtos)
    df_produtos_sem_duplicados = df_produtos.drop_duplicates(subset="Nome")

    df_produtos_sem_duplicados.to_csv("results/paguemenos/lista_produtos.csv", index=False)
get_Produtos()
driver.quit()
time.sleep(3)