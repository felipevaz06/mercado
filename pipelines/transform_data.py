import os
import pandas as pd
import re
import json
from collections import defaultdict
import spacy
from datetime import datetime

nlp = spacy.load("pt_core_news_sm")

paguemenos_base = 'results/paguemenos/paguemenos_01-05-2025.csv'
df_marca = pd.read_csv(paguemenos_base, sep=',')
print(df_marca.columns)
marcas = df_marca['Marca'].dropna().unique().tolist()



def extrair_data(nome_arquivo):
    match = re.search(r"\d{2}-\d{2}-\d{4}", nome_arquivo)
    return datetime.strptime(match.group(0), "%d-%m-%Y") if match else None

def extrair_peso(texto):
    match = re.search(r'(\d+[.,]?\d*)\s?(kg|g|l|ml)', texto.lower())
    if match:
        valor = match.group(1).replace(',', '.')  # troca vírgula por ponto
        unidade = match.group(2)
        return f"{valor}{unidade}"
    return None

def extrair_nome_composto(texto):
    texto = texto.lower()
    
    texto = re.sub(r'\s*-\s*', ' ', texto)

    texto = re.sub(r'\d+[.,]?\d*\s?(kg|g|ml|l|unidades?|c/|sachês?|caixa|garrafa|frasco|pacote|vidro|molheira|pet|unid.)', '', texto)
    
    texto = re.sub(r'\b(c/|-|com|sem|zero|preço|oferta|promoção|novo|especial|refrigerante|refil|pet|c/|spray|aerossol|leve|gratis)\b', '', texto)
    
    palavras = re.sub(r'\s+', ' ', texto).strip().split()

    if not palavras:
        return ''
    if len(palavras)>1 and (palavras[1]=="de" or palavras[1]=="em" or palavras[1]=="com" or palavras[1]=="para"):
        return f"{palavras[0]} {palavras[1]} {palavras[2]}"
    if len(palavras) == 1:
        return palavras[0]

    return f"{palavras[0]} {palavras[1]}"

def encontrar_marca(nome_produto):
    palavras = set(re.findall(r'\b\w+\b', nome_produto.lower()))
    for marca in marcas:
        if marca.lower() in palavras:
            return marca
    return None

def string_to_float(valor):
    if isinstance(valor, str):
        valor = valor.replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(valor)
    except ValueError:
        return None


def transform_data(mercados):
    produtos = defaultdict(lambda: {
        "nome": "",
        "marca": "",
        "categoria": "",
        "peso": "",
        "historico_precos": [],
        "mercados": set()
    })

    for mercado in mercados:
        arquivos = [f for f in os.listdir(mercado) if (f.startswith("paguemenos") or f.startswith("saovicente")) and f.endswith(".csv")]
        print(f"Processando arquivos em {mercado}: {arquivos}")
        for arquivo in arquivos:
            if arquivo.startswith("paguemenos"):
                supermercado = "Pague Menos"
            elif arquivo.startswith("saovicente"):
                supermercado = "São Vicente"
            else:
                continue  # ignora outros arquivos

            data_extracao = extrair_data(arquivo)
            if not data_extracao:
                continue  

            caminho_completo = os.path.join(mercado, arquivo)
            df = pd.read_csv(caminho_completo)

            for _, row in df.iterrows():
                nome = row.get("Nome")
                preco = string_to_float(row.get("Preço")) 
                if pd.isna(nome) or pd.isna(preco):
                    continue

                preco_info = {"data": data_extracao, "preco": preco, "supermercado": supermercado}
                produto = produtos[nome]

                if not produto["marca"]:
                    produto["marca"] = row.get("Marca") or encontrar_marca(nome)
                if not produto["categoria"]:
                    produto["categoria"] = str(row.get("Categoria", "")).strip().split('\n')[-1]
                if not produto["peso"]:
                    produto["peso"] = extrair_peso(nome)
                if not produto["nome"]:
                    produto["nome"] = extrair_nome_composto(nome)

                produto["historico_precos"].append(preco_info)
                produto["mercados"].add(supermercado)

    documentos = []
    for nome, dados in produtos.items():
        doc = {
            "nome_completo": nome,
            "nome": dados["nome"],
            "marca": dados["marca"],
            "categoria": dados["categoria"],
            "peso": dados["peso"],
            "mercados": list(dados["mercados"]),
            "historico_precos": sorted(dados["historico_precos"], key=lambda x: x["data"])
        }
        documentos.append(doc)


    print(f"{len(documentos)} produtos salvos.")
    return documentos

