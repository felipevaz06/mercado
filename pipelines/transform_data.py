import re
import unidecode
import pandas as pd

def preprocess_text(nomes):
    text = unidecode.unidecode(text.lower())
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df = pd.read_csv("../results/paguemenos/paguemenos_2025-04-13_13-49-08.csv")

nomes = df["Nome"]

lista=[]
for produto in nomes:
    lista.append(preprocess_text(produto))
print(lista)