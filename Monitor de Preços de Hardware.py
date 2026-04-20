from sys import exception
import requests
from bs4 import BeautifulSoup
import pandas as pd
import cloudscraper
from datetime import datetime
import math
from sqlalchemy import create_engine

linkProcessadorKabum = "https://www.kabum.com.br/produto/320797/processador-amd-ryzen-7-5700x-3-4ghz-4-6ghz-max-turbo-cache-36mb-am4-sem-video-100-100000926wof"
linkProcessadorTerabyte = "https://www.terabyteshop.com.br/produto/20813/processador-amd-ryzen-7-5700x-34ghz-46ghz-turbo-8-cores-16-threads-am4-sem-cooler-100-100000926wof"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'} #sumila que é humano

#kabum
pagKabum = requests.get(linkProcessadorKabum, headers=headers)
dadosKabum = BeautifulSoup(pagKabum.content, 'html.parser')

tituloKabum =  dadosKabum.find('h1', class_= "text-sm desktop:text-xl text-black-800 font-bold desktop:font-bold").get_text()
tituloKabum = tituloKabum[0:29]

precoKabum =  dadosKabum.find('b',class_= "text-xs font-bold text-black-700").get_text()
precoKabum = precoKabum[3:8]

precoKabum = precoKabum.replace(".","")
precoKabum = float(precoKabum)

#terabyte
scraper = cloudscraper.create_scraper() #simula um navegador
pagTerabyte = scraper.get(linkProcessadorTerabyte)

dadosTerabyte = BeautifulSoup(pagTerabyte.content, 'html.parser')

tituloTerabyte = dadosTerabyte.find('h1',class_= 'tit-prod').get_text()
tituloTerabyte = tituloTerabyte[0:29]

precoTerabyte = dadosTerabyte.find('p', id="valVista").get_text()
precoTerabyte = precoTerabyte[3:8]
precoTerabyte = precoTerabyte.replace(".","")
precoTerabyte = float(precoTerabyte)
precoTerabyte = float(math.ceil(precoTerabyte / 0.85))

dataPrompt = datetime.now().strftime("%d/%m/%y")

#Criando o df
listaDicProcessador = [{"Nome": tituloKabum,"Preco": precoKabum, "Data": dataPrompt, "Site": "Kabum"},
                    {"Nome":tituloTerabyte ,"Preco":precoTerabyte ,"Data":dataPrompt ,"Site":"Terabyte"}
       ]
df = pd.DataFrame(listaDicProcessador)
print(df)

#conectando ao db
try:
    engine = create_engine("mssql+pymssql://sa:1234@localhost:1433/Rastreador de Hardware")
    df.to_sql(name="rastreador_hardware",con=engine, if_exists='append',index=False)
    print("foi")

except exception as e:
    print("Falha ao conectar")
















