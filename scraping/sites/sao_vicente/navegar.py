from config import URLS

def entrar_site(driver):
    url = URLS["sao_vicente"]
    driver.get(url)
    driver.maximize_window()
    