import datetime   # This will be needed later
import os
import json

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGODB_URI = os.environ['MONGODB_URI']
client = MongoClient(MONGODB_URI)

db = client['mercado']
collection = db['produtos_geral']

def test_connection():
   try:
      client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
   except Exception as e:
      print(e)

def save_to_mongodb(produtos):
   nomes_completos = [p["nome_completo"] for p in produtos]

   mapa_existentes={}
   total = collection.count_documents({})
   if total ==0:
      print("Nenhum produto encontrado na base de dados.")
      collection.insert_many(produtos)
      print(f"{len(produtos)} produtos inseridos.")
   else:
      produtos_existentes = collection.find({"nome_completo": {"$in": nomes_completos}})
      mapa_existentes = {p["nome_completo"]: p for p in produtos_existentes}

      novos = []
      atualizacoes = []

      for produto in produtos:
         existente = mapa_existentes.get(produto["nome_completo"])
         if existente:
            datas_existentes = {h["data"] for h in existente.get("historico_precos", [])}
            novos_precos = [
                  p for p in produto.get("historico_precos", [])
                  if p["data"] not in datas_existentes
            ]
            if novos_precos:
                  atualizacoes.append((produto["nome_completo"], novos_precos))
         else:
            novos.append(produto)

      if novos:
         collection.insert_many(novos)
         print(f"{len(novos)} produtos novos inseridos.")

      for nome_completo, novos_precos in atualizacoes:
         collection.update_one(
            {"nome_completo": nome_completo},
            {"$push": {"historico_precos": {"$each": novos_precos}}}
         )
      print(f"{len(atualizacoes)} produtos atualizados com novos preços.")
