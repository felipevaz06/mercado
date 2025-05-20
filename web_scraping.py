from scraping.driver import get_driver
from scraping.sites import sao_vicente, paguemenos
from pipelines.save_to_csv import save_to_csv

def extrair_saovicente():
    driver = get_driver()
    sao_vicente.navegar.entrar_site(driver)
    produtos_sao_vicente = sao_vicente.extrair.extrair_produtosSV(driver)
    save_to_csv(produtos_sao_vicente, site_nome="saovicente")
    driver.quit()

def extrair_paguemenos():
    driver = get_driver()
    paguemenos.navegar.entrar_site(driver)
    produtos_paguemenos = paguemenos.extrair.extrair_produtosPM(driver)
    save_to_csv(produtos_paguemenos, site_nome="paguemenos")
    driver.quit()

int = input("Escolha o site para extrair dados (1 - Pague Menos, 2 - São Vicente): ")
if int == "1":
    extrair_paguemenos()
elif int == "2":
    extrair_saovicente()
else: 
    print("Opção inválida. Saindo do programa.")



