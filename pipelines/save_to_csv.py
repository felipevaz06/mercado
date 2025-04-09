import pandas as pd
import datetime

def save_to_csv(dados: list[dict], site_nome: str):
    if not dados:
        print(f" Nenhum dado para salvar para o site '{site_nome}'")
        return

    data_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho_arquivo = "results/"+f"{site_nome}/"+ f"{site_nome}_{data_str}.csv"
    df = pd.DataFrame(dados)
    df.to_csv(caminho_arquivo, index=False, encoding="utf-8-sig")