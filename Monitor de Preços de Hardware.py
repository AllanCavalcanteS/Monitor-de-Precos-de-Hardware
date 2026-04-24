import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import cloudscraper
from datetime import datetime
import math
from sqlalchemy import create_engine

#LINKS
linkProcessadorK = "https://www.kabum.com.br/produto/320797/processador-amd-ryzen-7-5700x-3-4ghz-4-6ghz-max-turbo-cache-36mb-am4-sem-video-100-100000926wof"
linsPlacaMaeK = "https://www.kabum.com.br/produto/165124/placa-mae-asus-tuf-gaming-a520m-plus-wifi-amd-am4-rgb-matx-ddr4-preto-90mb17f0-m0eay0"
linkMemoriaRamK = "https://www.kabum.com.br/produto/513723/memoria-ram-gamer-rise-mode-aura-rgb-32gb-2x16gb-3200mhz-ddr4-cl19-branco-rm-d4aw-32g-3200argb"

linkProcessadorT = "https://www.terabyteshop.com.br/produto/20813/processador-amd-ryzen-7-5700x-34ghz-46ghz-turbo-8-cores-16-threads-am4-sem-cooler-100-100000926wof"
linkPlacaMaeT = "https://www.terabyteshop.com.br/produto/18752/placa-mae-asus-tuf-gaming-a520m-plus-wifi-chipset-a520-amd-am4-matx-ddr4-90mb17f0-m0eay0"
linkMemoriaRamT = "https://www.terabyteshop.com.br/produto/16238/memoria-ddr4-corsair-vengeance-lpx-32gb-2x16gb-2400mhz-cmk32gx4m2a2400c16"

#HEADERS
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'} #sumila que é humano


#DEFS
def semDesconto(dados):
    valor = float(math.ceil(dados / 0.85))
    return valor

def tituloT(dados):
    titulo = dados.find('h1', class_='tit-prod').get_text()
    return titulo

def valorT(dados):
    valor = dados.find('p', id="valVista").get_text()
    valor  = limparValor(valor)
    valor = semDesconto(valor)
    return valor

def tituloK(dados):
    titulo = dados.find('h1', class_="text-sm desktop:text-xl text-black-800 font-bold desktop:font-bold").get_text()
    return titulo

def valorK(dados):
    valor = dados.find('b', class_="text-xs font-bold text-black-700").get_text()
    valor = limparValor(valor)
    return valor

def limparNomeProcessador(nome):
    padrao = r"AMD Ryzen \d \w+"
    busca = re.search(padrao, nome,re.IGNORECASE)
    return busca.group(0)

def limparNomePlacaMae(nome):
    padrao = r"ASUS TUF GAMING A520M-PLUS WIFI"
    busca = re.search(padrao, nome, re.IGNORECASE)
    return busca.group(0)

def limparNomeMemoriaRamT(nome):
    padrao = r"Corsair Vengeance.*\(2x16GB\).*2400MHz"
    busca = re.search(padrao,nome, re.IGNORECASE)
    return busca.group(0)

def limparNomeMemoriaRamK(nome):
    padrao = r"Rise Mode Aura.*32GB.*\(2x16GB\).*3200MHz"
    busca = re.search(padrao,nome, re.IGNORECASE)
    return busca.group(0)

def limparValor(valor):
    valor = valor.replace("R$","").replace(".", "").replace(",", ".").strip()
    valor = float(valor)
    return valor

def dadosSiteK(link):
    pagina = requests.get(link,headers=headers)
    dados = BeautifulSoup(pagina.content, 'html.parser')
    return dados

def dadosSiteT(link):
    scraper = cloudscraper.create_scraper()
    pagina = scraper.get(link)
    dados = BeautifulSoup(pagina.content, 'html.parser')
    return dados

#KABUM
try:
    dadosProcessadorK = dadosSiteK(linkProcessadorK)
    dadosPlacaMaeK = dadosSiteK(linsPlacaMaeK)
    dadosMemoriaRamK = dadosSiteK(linkMemoriaRamK)

except Exception as e:
    print("Link Kabum Invalido")
    dadosProcessadorK = None
    dadosPlacaMaeK = None
    dadosMemoriaRamK = None
else:
    print("Links Kabum ok")

#terabyte
try:
    dadosProcessadorT = dadosSiteT(linkProcessadorT)
    dadosPlacaMaeT = dadosSiteT(linkPlacaMaeT)
    dadosMemoriaRamT = dadosSiteT(linkMemoriaRamT)

except Exception as e:
    print("Link Terabyte Invalido")
    dadosProcessadorT = None
    dadosPlacaMaeT = None
    dadosMemoriaRamT = None
else:
    print("Links Terabyte ok")

#kabum
    #processador
tituloProcessadorK =  tituloK(dadosProcessadorK)
tituloProcessadorK = limparNomeProcessador(tituloProcessadorK)

valorProcessadorK =  valorK(dadosProcessadorK)

    #placaMae
tituloPlacaMaeK = tituloK(dadosPlacaMaeK)
tituloPlacaMaeK = limparNomePlacaMae(tituloPlacaMaeK)

valorPlacaMaeK = valorK(dadosPlacaMaeK)

    #MEMORIA RAM
tituloMemoriaRamK = tituloK(dadosMemoriaRamK)
tituloMemoriaRamK = limparNomeMemoriaRamK(tituloMemoriaRamK)

valorMemoriaRamK = valorK(dadosMemoriaRamK)

#terabyte
    #Processador
tituloProcessadorT = tituloT(dadosProcessadorT)
tituloProcessadorT = limparNomeProcessador(tituloProcessadorT)

valorProcessadorT = valorT(dadosProcessadorT)

    #placaMAE
tituloPlacaMaeT = tituloT(dadosPlacaMaeT)
tituloPlacaMaeT = limparNomePlacaMae(tituloPlacaMaeT)

valorPlacaMaeT = valorT(dadosPlacaMaeT)

    #MEMORIA RAM
tituloMemoriaRamT = tituloT(dadosMemoriaRamT)
tituloMemoriaRamT = limparNomeMemoriaRamT(tituloMemoriaRamT)

valorMemoriaRamT = valorT(dadosMemoriaRamT)

#Criando o df
dataPrompt = datetime.now()#.strftime("%d/%m/%y")


#Sites
kabum = "Kabum"
terabyte = "Terabyte"

#tipos
processador = "Processador"
placaMae = "Placa Mae"
memoriaRam = "Memoria Ram DDR4"

dadosFinal = [      {"Tipo":processador,"Nome":tituloProcessadorK,"Preco":valorProcessadorK,"Data":dataPrompt,"Site":kabum},
                    {"Tipo":processador,"Nome":tituloProcessadorT,"Preco":valorProcessadorT,"Data":dataPrompt,"Site":terabyte},
                    {"Tipo":placaMae,"Nome":tituloPlacaMaeK,"Preco":valorPlacaMaeK,"Data":dataPrompt,"Site":kabum},
                    {"Tipo":placaMae,"Nome":tituloPlacaMaeT,"Preco":valorPlacaMaeT,"Data":dataPrompt,"Site":terabyte},
                    {"Tipo":memoriaRam,"Nome":tituloMemoriaRamK,"Preco":valorMemoriaRamK,"Data":dataPrompt,"Site":kabum},
                    {"Tipo":memoriaRam,"Nome":tituloMemoriaRamT,"Preco":valorMemoriaRamT,"Data":dataPrompt,"Site":terabyte}
            ]
df = pd.DataFrame(dadosFinal)
print(df)

#conectando ao db
try:
    engine = create_engine("mssql+pymssql://sa:1234@localhost:1433/Rastreador de Hardware")
    df.to_sql(name="monitor_preco_hardware",con=engine, if_exists='append',index=False)
    print("Foi")

except Exception as e:
    print("Falha ao conectar")















