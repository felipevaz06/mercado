from config import URLS

def entrar_site(driver):
    url = URLS["pague_menos"]
    driver.get(url)
    driver.maximize_window()
    