import pandas as pd
from datetime import datetime

def save_to_csv(dados, site_nome: str):
    if not dados:
        print(f" Nenhum dado para salvar para o site '{site_nome}'")
        return

    data_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho_arquivo = "results/"+f"{site_nome}/"+ f"{site_nome}_{data_str}.csv"
    df = pd.DataFrame(dados)
    df_produtos_sem_duplicados = df.drop_duplicates(subset="Nome")
    df_produtos_sem_duplicados.to_csv(caminho_arquivo, index=False, encoding="utf-8-sig")