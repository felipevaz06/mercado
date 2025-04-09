from scraping.driver import get_driver
from scraping.sites import sao_vicente, paguemenos
from pipelines import save_to_csv
driver = get_driver()

# sao_vicente.navegar.entrar_site(driver)
# produtos_sao_vicente = sao_vicente.extrair.extrair_produtosSV(driver)
# save_to_csv(produtos_sao_vicente, site_nome="saovicente")

paguemenos.navegar.entrar_site(driver)
produtos_paguemenos = paguemenos.extrair.extrair_produtosPM(driver)

driver.quit()
